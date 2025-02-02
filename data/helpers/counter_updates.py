import json

# Original JSON data
with open('new_counters.json') as f:
    data = json.load(f)
    
# Update information from text file
with open('counter_updates.txt') as f:
    update_data = f.read().splitlines()


# Process updates
for line in update_data:
    if line.strip(): # skip empty lines
        key, tip = line.split(": ", 1)
        key = key.lower().strip()
        if key in data:
            data[key]["brawler_counters"] = tip.strip()
        else:
            print(f"Key not found: {key}")

# Convert to JSON format
formatted_json = json.dumps(data, indent=4)

# Save to file
with open("updates_counters.json", "w") as f:
    f.write(formatted_json)
