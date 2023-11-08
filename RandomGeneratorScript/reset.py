import os
import json
import rarfile
import zipfile

# List of valid faction tags
valid_faction_tags = [
    "pilot_davion",
    "pilot_marik",
    "pilot_liao",
    # ... (other valid faction tags) ...
    "pilot_worldofblake"
]

# Exceptions for tags
tag_exceptions = ["eyes", "handedness", "bloodtype", "stature"]

# Get the directory of the script
script_directory = os.path.dirname(__file__)

# Directory paths
input_directory = os.path.join(script_directory, "PilotGeneration")
output_directory = os.path.join(script_directory, "..", "PilotPerkOverhaul", "Pilots")
revert_zip_file = os.path.join(script_directory, "..", "PilotPerkOverhaul", "Pilots", "revert.zip")

# Delete existing JSON files in the "Pilots" folder
for filename in os.listdir(output_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(output_directory, filename)
        os.remove(file_path)

# Delete existing JSON files in the "PilotGeneration" folder
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(input_directory, filename)
        os.remove(file_path)

# Extract and copy JSON files from "revert.zip" to "Pilots" folder
with zipfile.ZipFile(revert_zip_file, "r") as zip_file:
    for zip_info in zip_file.infolist():
        if zip_info.filename.endswith(".json"):
            extracted_tags = json.loads(zip_file.read(zip_info.filename))
            with open(os.path.join(output_directory, zip_info.filename), "w") as output_file:
                json.dump(extracted_tags, output_file, indent=4)
                print(f"Replaced {zip_info.filename}")

print("All JSON files have been replaced with fresh copies.")