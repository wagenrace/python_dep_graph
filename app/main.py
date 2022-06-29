import os

from fastapi import FastAPI
from py2neo import Graph

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = os.environ["NEO4J_URL"]
user = os.environ["NEO4J_USER"]
pswd = os.environ["NEO4J_PSWD"]

graph = Graph(url, auth=(user, pswd))


@app.post("/getPackagesInfoV2/")
async def read_item(package_names: list):
    response = graph.run(
        f"""
            MATCH (n:Package)-[:DEPENDS_ON*0..]->(m:Package)
            WHERE n.name in {package_names}
            WITH DISTINCT m as p
            RETURN DISTINCT p.license as licenses, collect(p.name) as packageNames, sum(p.package_size) as totalSizeBytes
        """
    ).data()

    # Not all packages will be found
    all_found_packages = []
    for i in response:
        all_found_packages += i["packageNames"]

    all_not_found_packages = []

    for package_name in package_names:
        if not package_name in all_found_packages:
            all_not_found_packages.append(package_name)

    if len(all_not_found_packages):
        response.append(
            {
                "licenses": "NOT FOUND",
                "packageNames": all_not_found_packages,
                "totalSizeBytes": 0,
            },
        )
    return response
