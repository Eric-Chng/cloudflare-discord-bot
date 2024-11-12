import json
import os
from thefuzz import process

# Get the path to the directory containing add_builds.py
current_dir = os.path.dirname(__file__)

# Construct paths to the JSON files
builds_json_path = os.path.join(current_dir, '../builds.json')
builds_s32_json_path = os.path.join(current_dir, 'replacement.json')

with open(builds_json_path, 'r') as f:
    builds = json.load(f)
with open(builds_s32_json_path, 'r') as f:
    builds32 = json.load(f)

def highest_fuzzy_match_on_keys(json_data, search_term):
    best_match = None
    highest_score = 0
    best_key = None
    
    search_term = search_term.lower()
    

    for key, value in json_data.items():
        # Extract all keys from the item and join them into a single string
        keys_text = key

        # Perform fuzzy matching and check if it's the highest score
        match_score = process.extractOne(search_term, [keys_text])[1]

        if match_score > highest_score:
            highest_score = match_score
            best_key = key
            best_match = value

    return best_key, best_match, highest_score

# Building a new json file with the new builds
new_builds = {}

for key, value in builds32.items():
    res_key, res_match, score = highest_fuzzy_match_on_keys(builds, key)
    # if value has a key "tips" then add it to the new_builds
    if "tips" in value:
        if "hypercharge" in value["tips"].lower():
            res_match["hypercharge"] = value["tips"]
            print(f"Added hypercharge to {res_key}")
        else:
            print(f"Hypercharge not found in {res_key}")
    if "tip" in value:
        if "hypercharge" in value["tip"].lower():
            res_match["hypercharge"] = value["tip"]
            print(f"Added hypercharge to {res_key}")
        else:
            print(f"Hypercharge not found in {res_key}")
    res_match["gadget"] = value["gadget"]
    res_match["gear"] = value["gear"]
    res_match["starpower"] = value["starpower"]
    new_builds[res_key] = res_match

# Write the new builds to a file
new_builds_path = os.path.join(current_dir, 'output.json')
with open(new_builds_path, 'w') as f:
    json.dump(new_builds, f, indent=4)