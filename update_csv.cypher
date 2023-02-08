LOAD CSV WITH HEADERS FROM 'http://csv_proxy/wagenrace/python_dep_graph/upgrade_to_all/all_packages.csv' AS row
WITH row
WHERE NOT row.name IS null
MERGE (n:package {name: row.name})
SET n.license= row.license
SET n.package_size = row.package_size
