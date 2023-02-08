LOAD CSV WITH HEADERS FROM 'http://csv_proxy/wagenrace/python_dep_graph/upgrade_to_all/all_dependencies.csv' AS row
WITH row
WHERE NOT row.package IS null AND NOT row.dependsOn
MATCH (n:package {name: row.package})
MATCH (n2:package2 {name: row.dependsOn})
MERGE (n)-[:MATCH]->(n2)