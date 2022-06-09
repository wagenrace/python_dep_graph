import os

from fastapi import FastAPI
from py2neo import Graph

app = FastAPI()

url = os.environ["NEO4J_URL"]
user = os.environ["NEO4J_USER"]
pswd = os.environ["NEO4J_PSWD"]

graph = Graph(url, auth=(user, pswd))


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/getPackagesInfo/")
async def read_item(package_names: list):
    response = graph.run(
        f"""
            MATCH (n:Package)-[:DEPENDS_ON*0..]->(m:Package)
            WHERE n.name in {package_names}
            WITH DISTINCT m as p
            RETURN collect(p.name) as packageNames, collect(DISTINCT p.license) as licenses, sum(p.size) as totalSizeBytes"""
    ).data()[0]

    return response
