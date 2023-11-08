import os
import json
import zipfile
import random

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

# Data
pilots = {
    "Green": ["Bono", "FalkM", "Heysek", "Hollabaugh", "Jakes", "Korwes", "Miller", "Piazza", "Ryia", "Shvartz", "Slipais", "SwansonA", "Thomas", "Voyls", "Gibbs", "Godfrey", "Leone", "Liebenow", "Saada", "Sampson", "Woods", "Oliver", "Shields"],
    "Regular": ["Cochran", "Kaufman", "Loving", "Reichenbach", "Bixby", "Bozeman", "Brewer", "Brown", "Cleary", "Doukas", "Durand", "Eck", "Fielding", "Hording", "Hurtado", "Keane", "Lemos", "Mzik", "Nick"],
    "Veteran": ["Test9", "Archangel", "Reinke", "Alaniz", "Bemis", "Chang", "Chik", "Chung", "Coldfire", "Doochin", "Eckett", "Endorf", "FalkA", "Hardie", "Helterbran", "Hill", "Huxley"],
    "Elite": ["Apex", "Arclight", "Blockade", "Buckshot", "Kraken", "Mockingbird", "Ozone", "Paradise", "Showboat", "Squire", "Sumo", "Wildfire"],
}

# Sort the pilots by category and name
sorted_pilots = [(category, name) for category, names in pilots.items() for name in sorted(names)]

# Perk categories
perk_categories = {
    "Positive": [
        "pilot_assassin", "pilot_athletic", "pilot_commander", "pilot_ex-comstar", "pilot_lostech", "pilot_merchant", "pilot_military", "pilot_spacer",
        "pilot_technician", "pilot_resilient", "pilot_gunslinger", "pilot_deadeye", "pilot_gladiator", "pilot_officer", "pilot_brave", "pilot_inconspicuous",
        "pilot_calm", "pilot_lucky"
    ],
    "Mixed": [
        "pilot_bookish", "pilot_cautious", "pilot_criminal", "pilot_dependable",
        "pilot_dishonest", "pilot_drunk", "pilot_reckless", "pilot_honest",
        "pilot_noble", "pilot_bushido", "pilot_zealot", "pilot_feral", "pilot_redline"
    ],
    "Negative": [
        "pilot_klutz", "pilot_nervous", "pilot_fragile", "pilot_apathetic",
        "pilot_lazyeye", "pilot_traumatic_injury", "pilot_nearsighted",
        "pilot_limitedvision", "pilot_conspicuous", "pilot_pretentious",
        "pilot_reject","pilot_jinxed"
    ],
}

# Characteristics
characteristics = {
    "Eyes": ["eyes_heterochromatic", "eyes_brown", "eyes_blue", "eyes_green", "eyes_hazel"],
    "Handedness": ["handedness_right", "handedness_left", "handedness_ambidextrous"],
    "Blood Type": ["bloodtype_b_positive", "bloodtype_a_negative", "bloodtype_o_positive", "bloodtype_a_positive", "bloodtype_ab_negative", "bloodtype_ab_positive", "bloodtype_o_negative"],
    "Stature": ["stature_average", "stature_tall", "stature_above_average", "stature_short", "stature_below_average"],
}

# Output folder for JSON files relative to the script's location
output_folder = os.path.join(script_directory, "PilotGeneration")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to generate perks for a pilot
def generate_perks(pilot_category):
    perks = {
        "Positive": [],
        "Mixed": [],
        "Negative": [],
    }

    # Define handedness percentages
    handedness_percentages = {
        "Right": 0.75,
        "Left": 0.15,
        "Ambidextrous": 0.10,
    }

    # Minimum perks required for each category
    min_perks = {
        "Green": (1, 0, 0),
        "Regular": (1, 0, 0),
        "Veteran": (1, 1, 0),
        "Elite": (2, 1, 0),
    }

    min_positive, min_mixed, min_negative = min_perks[pilot_category]

    # Roll for additional perks with rate limits
    for _ in range(min_positive + (random.random() < 0.2)):
        perk = random.choice(perk_categories["Positive"])
        if perk not in perks["Positive"]:
            perks["Positive"].append(perk)
    for _ in range(min_mixed + (random.random() < 0.3)):
        perk = random.choice(perk_categories["Mixed"])
        if perk not in perks["Mixed"]:
            perks["Mixed"].append(perk)
    for _ in range(min_negative + (random.random() < 0.4)):
        perk = random.choice(perk_categories["Negative"])
        if perk not in perks["Negative"]:
            perks["Negative"].append(perk)

    # Randomly select characteristics
    pilot_characteristics = {
        "Eyes": random.choice(characteristics["Eyes"]),
        "Handedness": random.choices(list(handedness_percentages.keys()), weights=list(handedness_percentages.values()))[0],
        "Blood Type": random.choice(characteristics["Blood Type"]),
        "Stature": random.choice(characteristics["Stature"]),
    }

    return perks, pilot_characteristics

# Output for individual pilot information
output = []

# Generate perks and characteristics for each pilot
for pilot_category, pilot_name in sorted_pilots:
    pilot_perks, pilot_characteristics = generate_perks(pilot_category)

    # Determine the appropriate prefix
    if pilot_name in ["Apex", "Arclight", "Blockade", "Buckshot", "Kraken", "Mockingbird", "Ozone", "Paradise", "Showboat", "Squire", "Sumo", "Wildfire"]:
        pilot_prefix = "pilot_ronin"
    else:
        pilot_prefix = "pilot_backer"

    # Create a dictionary for each pilot's information
    pilot_info = {
        "Id": f"{pilot_prefix}_{pilot_name}",
        "PilotTags": {
            "items": [
                f"eyes_{pilot_characteristics['Eyes'].lower()}",
                f"handedness_{pilot_characteristics['Handedness'].lower()}",
                f"bloodtype_{pilot_characteristics['Blood Type'].replace('+', '_positive').replace('-', '_negative').lower()}",
                f"stature_{pilot_characteristics['Stature'].lower()}",
            ]
        }
    }

    # Add the "pilot_" prefix only to perk tags
    traits = ["pilot_" + trait.lower() if not trait.startswith("pilot_") else trait.lower() for trait in pilot_perks["Positive"] + pilot_perks["Mixed"] + pilot_perks["Negative"]]
    pilot_info["PilotTags"]["items"].extend(traits)

    output.append(pilot_info)  # Append the pilot information dictionary to the output list

# Output JSON files for each pilot
for pilot_data in output:
    pilot_id = pilot_data["Id"]
    output_file = os.path.join(output_folder, f"{pilot_id}.json")
    with open(output_file, "w") as file:
        json.dump(pilot_data, file, indent=4)
        print(f"JSON file created for {pilot_id} in '{output_file}'")

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

                # Merge PilotTags items without duplicates and with correct prefixes
                if "PilotTags" in pilots_data and "PilotTags" in pilot_generation_data:
                    pilot_tags_existing = pilots_data["PilotTags"]["items"]
                    pilot_tags_new = pilot_generation_data["PilotTags"]["items"]

                    # Merge the tags, ensuring there are no duplicates and adding the correct prefixes
                    pilot_tags_merged = []

                    for tag in pilot_tags_new:
                        # Remove the extra prefixes
                        if tag.startswith("eyes_"):
                            tag = tag[len("eyes_"):]
                        elif tag.startswith("handedness_"):
                            tag = tag[len("handedness_"):]
                        elif tag.startswith("bloodtype_"):
                            tag = tag[len("bloodtype_"):]
                        elif tag.startswith("stature_"):
                            tag = tag[len("stature_"):]

                        # Add the correct prefix
                        if tag not in pilot_tags_existing:
                            if tag == "left" or tag == "right" or tag == "ambidextrous":
                                tag = f"handedness_{tag}"
                            pilot_tags_merged.append(tag)

                    pilots_data["PilotTags"]["items"].extend(pilot_tags_merged)

                # Write the updated data back to the Pilots file
                with open(pilots_file_path, "w") as pilots_file:
                    json.dump(pilots_data, pilots_file, indent=4)

                print(f"PilotTags merged successfully for {filename}")


                # Write the updated data back to the Pilots file
                with open(pilots_file_path, "w") as pilots_file:
                    json.dump(pilots_data, pilots_file, indent=4)

                print(f"PilotTags merged successfully for {filename}")


# Call the function to merge PilotTags for all files
merge_pilot_tags_for_files(output_directory, output_folder)