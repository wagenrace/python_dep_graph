import json
import os

current_loc = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(current_loc, "licenses_synonyms.json"), "r") as f:
    LICENSES_SYNONYMS = json.load(f)

def get_license(data: dict):
    # Get license
    license = None
    classifiers = data["info"].get("classifiers", [])
    for classifier in classifiers:
        if not classifier.lower().startswith("license"):
            continue
        l = classifier.split(" :: ")[-1]
        if l in ['OSI Approved',  'LICENSE.txt']:
            continue
        license = l
        break

    if not license:
        license = data["info"].get("license")
        if " :: " in license:
            license = license.split(" :: ")[-1]
    
    if len(license) > 300:
        license = license[:300]
    
    license = license if license else f"UNKNOWN"
    license = LICENSES_SYNONYMS.get(license.lower(), license)
    return license
