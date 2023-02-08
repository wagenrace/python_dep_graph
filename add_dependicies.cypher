LOAD CSV WITH HEADERS FROM 'http://csv_proxy/wagenrace/python_dep_graph/upgrade_to_all/all_dependencies.csv' AS row
WITH row
WHERE NOT row.package IS null AND NOT row.dependsOn IS null
MATCH (n:Package {name: row.package})
MATCH (n2:Package {name: row.dependsOn})
MERGE (n)-[:DEPENDS_ON]->(n2)