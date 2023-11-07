import os
import json

# List of valid faction tags
valid_faction_tags = [
    "pilot_davion",
    "pilot_marik",
    "pilot_liao",
    "pilot_kurita",
    "pilot_steiner",
    "pilot_periphery",
    "pilot_tortuga",
    "pilot_taurian",
    "pilot_magistracy",
    "pilot_aurigan",
    "pilot_bloodspirit",
    "pilot_burrock",
    "pilot_circinus",
    "pilot_cloudcobra",
    "pilot_coyote",
    "pilot_diamondshark",
    "pilot_firemandrill",
    "pilot_ghostbear",
    "pilot_goliathscorpion",
    "pilot_hellshorses",
    "pilot_icehellion",
    "pilot_illyria",
    "pilot_ives",
    "pilot_lothian",
    "pilot_marian",
    "pilot_novacat",
    "pilot_oberon",
    "pilot_outworld",
    "pilot_smokejaguar",
    "pilot_snowraven",
    "pilot_solaris",
    "pilot_staradder",
    "pilot_steelviper",
    "pilot_tortuga",
    "pilot_valkyrate",
    "pilot_wolf",
    "pilot_worldofblake"
]

# Directory paths
input_directory = "C:/Users/Silver/Documents/GitHub/White-Fire/PilotPerkOverhaul/RandomGeneratorScript/PilotGeneration"
output_directory = "C:/Users/Silver/Documents/GitHub/White-Fire/PilotPerkOverhaul/PilotPerkOverhaul/Pilots"

# Iterate through JSON files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        # Read the JSON file from the input directory
        input_json_file_path = os.path.join(input_directory, filename)
        with open(input_json_file_path, "r") as input_file:
            input_data = json.load(input_file)
        
        # Extract data from "PilotTags" field
        if "PilotTags" in input_data and "items" in input_data["PilotTags"]:
            extracted_tags = input_data["PilotTags"]["items"]
            
            # Search for a matching JSON file in the output directory
            matching_output_file_path = os.path.join(output_directory, filename)
            
            if os.path.exists(matching_output_file_path):
                # Read the matching JSON file from the output directory
                with open(matching_output_file_path, "r") as output_file:
                    output_data = json.load(output_file)
                
                # Update the "PilotTags" field in the output JSON
                if "PilotTags" in output_data and "items" in output_data["PilotTags"]:
                    # Append the extracted tags to the existing tags
                    existing_tags = output_data["PilotTags"]["items"]
                    existing_tags.extend(extracted_tags)
                    # Remove duplicates by converting to a set and back to a list
                    existing_tags = list(set(existing_tags))
                    output_data["PilotTags"]["items"] = existing_tags
                
                # Write the updated data back to the output JSON file
                with open(matching_output_file_path, "w") as output_file:
                    json.dump(output_data, output_file, indent=4)
                
                print(f"Modified {filename}")
            else:
                print(f"No matching JSON file found for {filename}")
        else:
            print(f"No data found in {filename}")

print("All JSON files have been processed.")