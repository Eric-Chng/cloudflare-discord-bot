import json
import os

# Load JSON files
current_dir = os.path.dirname(__file__)
files = ["builds.json", "counters.json", "drafts.json", "modifiers.json"]

# Load and print JSON data to text file
output_lines = []
for file in files:
    file_path = os.path.join(current_dir, file)
    with open(file_path, "r") as f:
        data = json.load(f)
    if len(output_lines) == 0:
        output_lines.append("Brawl Stars Data\n")
    else:
        output_lines.append("\n\n")
    output_lines.append(f"--- {file} ---\n")
    for key, value in data.items():
        line_to_append = ""
        if file == "builds.json":
            line_to_append = f"The brawler build for {key}. To build the brawler {key}: Gadgets = {value['gadget']}, Gears = {value['gear']}, Star powers = {value['starpower']}"
        elif file == "counters.json":
            line_to_append = f"Counter info for the brawler {key}. To counter the brawler {key}: {value}"
        elif file == "drafts.json":
            line_to_append = f"Draft info for the map {key}. To draft the map {key}: {value}"
        elif file == "modifiers.json":
            line_to_append = f"Draft info for the map modifier {key}. To play the map modifier {key}: {value}"
        output_lines.append(line_to_append + "\n")

# Write to text file
output_path = os.path.join(current_dir, "brawlstars_textified.txt")
with open(output_path, "w") as output_file:
    output_file.writelines(output_lines)

print(f"Data exported to {output_path}")

