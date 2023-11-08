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
    "pilot_hellhorses",
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

# List of valid perk tags
valid_perk_tags = [
    "pilot_assassin",
    "pilot_athletic",
    "pilot_bookish",
    "pilot_brave",
    "pilot_cautious",
    "pilot_command",
    "pilot_criminal",
    "pilot_dependable",
    "pilot_disgraced",
    "pilot_dishonest",
    "pilot_drunk",
    "pilot_excomstar",
    "pilot_gladiator",
    "pilot_honest",
    "pilot_jinxed",
    "pilot_klutz",
    "pilot_lostech",
    "pilot_lucky",
    "pilot_mechwarrior",
    "pilot_merchant",
    "pilot_military",
    "pilot_noble",
    "pilot_officer",
    "pilot_reckless",
    "pilot_spacer",
    "pilot_tech",
    "pilot_wealthy",
    "pilot_engspecialist",
    "pilot_balspecialist",
    "pilot_mslspecialist",
    "pilot_indspecialist",
    "pilot_heatspecialist",
    "pilot_lamspecialist",
    "pilot_novice_technician",
    "pilot_adv_technician",
    "pilot_master_technician",
    "pilot_nervous",
    "pilot_bushido",
    "pilot_zealot",
    "pilot_resilient",
    "pilot_fragile",
    "pilot_apathetic",
    "pilot_lazyeye",
    "pilot_gunslinger",
    "pilot_deadeye",
    "pilot_traumatic_injury",
    "pilot_nearsighted",
    "pilot_limitedvision",
    "pilot_conspicuous",
    "pilot_pretentious",
    "pilot_reject",
    "pilot_inconspicuous",
    "pilot_calm",
    "pilot_feral",
    "pilot_redline",
    "pilot_quad_training",
    "pilot_tank_training",
    "pilot_reserve"
]

import os
import json

# List of valid faction tags
valid_faction_tags = [
    "pilot_davion",
    "pilot_marik",
    # Add more valid faction tags as needed
]

# List of valid perk tags
valid_perk_tags = [
    "pilot_assassin",
    "pilot_athletic",
    # Add more valid perk tags as needed
]

# Exceptions for tags
tag_exceptions = ["eyes", "handedness", "bloodtype", "stature"]

import os
import json

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the input and output directories
pilots_directory = os.path.join(script_directory, "..", "PilotPerkOverhaul", "Pilots")
pilot_generation_directory = os.path.join(script_directory, "PilotGeneration")

# Function to merge PilotTags from PilotGeneration files into Pilots files
def merge_pilot_tags_for_files(pilots_directory, pilot_generation_directory):
    # Iterate through the files in the Pilots directory
    for filename in os.listdir(pilots_directory):
        if filename.endswith(".json"):
            pilots_file_path = os.path.join(pilots_directory, filename)
            pilot_generation_file_path = os.path.join(pilot_generation_directory, filename)

            if os.path.exists(pilot_generation_file_path):
                # Read data from the Pilots file
                with open(pilots_file_path, "r") as pilots_file:
                    pilots_data = json.load(pilots_file)

                # Read data from the PilotGeneration file
                with open(pilot_generation_file_path, "r") as pilot_generation_file:
                    pilot_generation_data = json.load(pilot_generation_file)

                # Merge PilotTags items without duplicates
                if "PilotTags" in pilots_data and "PilotTags" in pilot_generation_data:
                    pilot_tags_existing = pilots_data["PilotTags"]["items"]
                    pilot_tags_new = pilot_generation_data["PilotTags"]["items"]
                    pilot_tags_merged = []

                    # Add preexisting tags at the beginning
                    pilot_tags_merged.extend(tag for tag in pilot_tags_existing if tag in ["name_Dragon_66", "pilot_davion"])
                    
                    # Add tags with specific prefixes first
                    prefix_order = ["bloodtype_", "eyes_", "handedness_", "stature_"]
                    for prefix in prefix_order:
                        for tag in pilot_tags_new:
                            if tag.startswith(prefix) and tag not in pilot_tags_merged:
                                pilot_tags_merged.append(tag)

                    # Add any remaining tags
                    for tag in pilot_tags_new:
                        if tag not in pilot_tags_merged:
                            pilot_tags_merged.append(tag)

                    # Add any existing tags not already in the list
                    for tag in pilot_tags_existing:
                        if tag not in pilot_tags_merged:
                            pilot_tags_merged.append(tag)

                    pilots_data["PilotTags"]["items"] = pilot_tags_merged

                # Write the updated data back to the Pilots file
                with open(pilots_file_path, "w") as pilots_file:
                    json.dump(pilots_data, pilots_file, indent=4)

                print(f"PilotTags merged successfully for {filename}")

# Call the function to merge PilotTags for all files
merge_pilot_tags_for_files(pilots_directory, pilot_generation_directory)