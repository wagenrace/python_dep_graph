#%%
import re

import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

from app.scrap_helpers import get_license

all_packages = {}
all_start_packages = ["tomni", "neo4j"]
deps_on = []

url = r"https://pypi.org/simple/"
r = requests.get(url)
html_content = r.text
soup = BeautifulSoup(html_content, "lxml")

all_a = soup.find_all("a")

all_start_packages = [a.text for a in all_a]


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

    except:
        pass


for start_package in tqdm(all_start_packages):
    add_package(start_package)

all_packages_pd = pd.DataFrame(all_packages).transpose()
all_packages_pd.index.name = "name"
deps_on_pd = pd.DataFrame(deps_on, index=None)

all_packages_pd.to_csv("all_packages.csv")
deps_on_pd.to_csv("all_dependencies.csv", index=False)
