import json
import os
from thefuzz import process

# Get the path to the directory containing add_builds.py
current_dir = os.path.dirname(__file__)

# Construct paths to the JSON files
drafts_file_path = os.path.join(current_dir, 'new_drafts.json')

with open(drafts_file_path, 'r') as f:
    drafts = json.load(f)
    

# Load ../drafts.json
drafts_path = os.path.join(current_dir, '../drafts.json')
with open(drafts_path, 'r') as f:
    old_drafts = json.load(f)


# Iterate new drafts
for key, value in drafts.items():
    old_drafts[key] = value


# Write the new builds to a file
new_builds_path = os.path.join(current_dir, 'output.json')
with open(new_builds_path, 'w') as f:
    json.dump(old_drafts, f, indent=4)