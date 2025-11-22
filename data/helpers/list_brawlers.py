import json
import os

# Get the path to builds.json relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
builds_path = os.path.join(script_dir, '..', 'builds.json')

# Read and parse the JSON file
with open(builds_path, 'r') as f:
    builds_data = json.load(f)

# Get all keys and output as comma-separated list
brawler_names = list(builds_data.keys())
print(', '.join(brawler_names))

