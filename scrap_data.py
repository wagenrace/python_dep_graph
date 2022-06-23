#%%
import re

import pandas as pd
import requests
from tqdm import tqdm

from app.scrap_helpers import get_license

all_packages = {}
all_start_packages = ["tomni", "neo4j"]
deps_on = []

response = requests.get(
    r"https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
)
top5000 = response.json()["rows"]

for top_package in top5000:
    all_start_packages.append(top_package["project"])


def add_package(package_name: str):
    try:
        if not package_name:
            return

        # If the package is already added stop
        if all_packages.get(package_name):
            return
        url = "https://pypi.python.org/pypi/" + str(package_name) + "/json"
        data = requests.get(url).json()

        raw_deps = data["info"].get("requires_dist", [])
        raw_deps = raw_deps if raw_deps else []
        package_size = max([i["size"] for i in data["urls"]])

        # Get license
        license = get_license(data)
        all_packages[package_name] = {
            "license": license,
            "package_size": package_size,
        }

        deps = []
        for raw_dep in raw_deps:
            if "extra == " in raw_dep:
                continue
            dep = re.search("[a-zA-Z0-9\-\_\.]*", raw_dep).group().lower()
            deps.append(dep)

        for dep in set(deps):
            deps_on.append({"package": package_name, "dependsOn": dep})
            add_package(dep)
    except:
        print(f"Error with {package_name}")


for start_package in tqdm(all_start_packages):
    add_package(start_package)

all_packages_pd = pd.DataFrame(all_packages).transpose()
all_packages_pd.index.name = "name"
deps_on_pd = pd.DataFrame(deps_on, index=None)

all_packages_pd.to_csv("all_packages.csv")
deps_on_pd.to_csv("all_dependencies.csv", index=False)
