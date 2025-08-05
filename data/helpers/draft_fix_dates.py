import json
import os
from thefuzz import process

# Get the path to the directory containing add_builds.py
current_dir = os.path.dirname(__file__)

# Load ../drafts.json
drafts_path = os.path.join(current_dir, '../drafts.json')
with open(drafts_path, 'r') as f:
    old_drafts = json.load(f)

maps = ["Dry Season", "Hideout", "Layer Cake", "Shooting Star", "Center Stage", "Pinball Dreams", "Sneaky Fields", "Triple Dribble", "Crystal Arcade", "Deathcap Trap", "Double Swoosh", "Gem Fort", "Hard Rock Mine", "Undermine", "Bridge too far", "Hot Potato", "Kaboom Canyon", "Safe Zone", "Dueling Beetles", "Open Business", "Parallel Plays", "Ring Of Fire", "Belles Rock", "Flaring Phoenix", "New Horizons", "Out in the open"]
#make sure all maps are in lower case
maps = [map.lower() for map in maps]

# Iterate new items
for key in maps:
    if key not in old_drafts:
        print(f"Draft for {key} not found in old_drafts.")
        break

# iterate old drafts
for key, value in old_drafts.items():
    if key not in maps:
        # remove last_updated field if it exists
        if "last_updated" in value:
            del value["last_updated"]
        old_drafts[key] = value

# Write the updated drafts to a file
updated_drafts_path = os.path.join(current_dir, 'updated_drafts.json')
with open(updated_drafts_path, 'w') as f:
    json.dump(old_drafts, f, indent=4)
