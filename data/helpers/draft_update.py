import json
import os

# Constants
LAST_UPDATED = "Nov 22, 2025"

# Get the path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths to the JSON files
new_drafts_path = os.path.join(script_dir, 'new_drafts.json')
old_drafts_path = os.path.join(script_dir, '..', 'drafts.json')
output_path = os.path.join(script_dir, 'output.json')

# Load new_drafts.json
with open(new_drafts_path, 'r') as f:
    new_drafts = json.load(f)

# Load drafts.json
with open(old_drafts_path, 'r') as f:
    old_drafts = json.load(f)

# Iterate new drafts and update old drafts
for key, value in new_drafts.items():
    # Initialize the map entry if it doesn't exist
    if key not in old_drafts:
        old_drafts[key] = {}
    
    # Update tips if present
    if "tips" in value and value["tips"] is not None and value["tips"] != "":
        old_drafts[key]["tips"] = value["tips"]
    
    # Update link if present
    if "link" in value and value["link"] is not None and value["link"] != "":
        old_drafts[key]["link"] = value["link"]
    
    # Set last_updated
    old_drafts[key]["last_updated"] = LAST_UPDATED

# Write the updated drafts to output.json
with open(output_path, 'w') as f:
    json.dump(old_drafts, f, indent=4)

print("✓ Successfully updated drafts to output.json")
print("\nReminder: Run 'python scripts/generate_system_prompt.py' to regenerate the system prompt with updated draft info.")