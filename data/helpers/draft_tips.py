import json
import os
from thefuzz import process

# Get the path to the directory containing add_builds.py
current_dir = os.path.dirname(__file__)

# Construct paths to the JSON files
drafts_file_path = os.path.join(current_dir, 'new_drafts.json')

with open(drafts_file_path, 'r') as f:
    drafts = json.load(f)


# Building a new json file with the new builds
new_builds = {}

for key, value in drafts.items():
    # if value has a key "tips" then add it to the new_builds
    map_value = {}
    if "tips" in value:
        map_value["tips"] = value["tips"]
    if "s31 tips" in value:
        map_value["tips"] = value["s31 tips"]
    if "link" in value:
        map_value["link"] = value["link"]
    else:
        print("No link for " + key)
    new_builds[key] = map_value

# Write the new builds to a file
new_builds_path = os.path.join(current_dir, 'output.json')
with open(new_builds_path, 'w') as f:
    json.dump(new_builds, f, indent=4)