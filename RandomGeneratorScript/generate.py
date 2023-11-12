import os
import json
import zipfile
import random

# List of valid faction tags
faction_tags = [
    "pilot_aurigan", "pilot_bloodspirit.json", "pilot_burrock.json", "pilot_circinus.json", "pilot_cloudcobra.json",
    "pilot_comstar", "pilot_coyote.json", "pilot_davion", "pilot_diamondshark.json", "pilot_firemandrill.json",
    "pilot_ghostbear.json", "pilot_goliathscorpion.json", "pilot_hellshorses.json", "pilot_icehellion.json",
    "pilot_illyria.json", "pilot_ives.json", "pilot_kurita", "pilot_liao", "pilot_lothian.json", "pilot_magistracy",
    "pilot_marian.json", "pilot_marik", "pilot_novacat.json", "pilot_outworld.json",
    "pilot_periphery", "pilot_smokejaguar.json", "pilot_snowraven.json", "pilot_solaris.json",
    "pilot_staradder.json", "pilot_steiner", "pilot_steelviper.json", "pilot_taurian", "pilot_tortuga.json",
    "pilot_valkyrate.json", "pilot_wolf.json", "pilot_worldofblake.json"
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
    "Regular": ["Cochran", "Kaufman", "Loving", "Reichenbach", "Bixby", "Bozeman", "Brewer", "Brown", "Cleary", "Doukas", "Durand", "Eck", "Fielding", "Hording", "Hurtado", "Keane", "Lemos", "Mzik", "Nick","SwansonK","Reidinger"],
    "Veteran": ["Test9", "Archangel", "Reinke", "Alaniz", "Bemis", "Chang", "Chik", "Chung", "Coldfire", "Doochin", "Eckett", "Endorf", "FalkA", "Hardie", "Helterbran", "Hill", "Huxley","Metke"],
    "Elite": ["Apex", "Arclight", "Blockade", "Buckshot", "Kraken", "Mockingbird", "Ozone", "Paradise", "Showboat", "Squire", "Sumo", "Wildfire","Witness"],
}

# Sort the pilots by category and name
sorted_pilots = [(category, name) for category, names in pilots.items() for name in sorted(names)]

# Perk categories
perk_categories = {
   "Positive": [
        "pilot_assassin", "pilot_athletic", "pilot_command", "pilot_ex-comstar", "pilot_lostech", "pilot_merchant", "pilot_military", "pilot_spacer",
        "pilot_technician", "pilot_resilient", "pilot_gunslinger", "pilot_deadeye", "pilot_gladiator", "pilot_officer", "pilot_brave", "pilot_inconspicuous",
        "pilot_calm", "pilot_lucky","pilot_momentum","pilot_tough","pilot_anchored","pilot_thrustvector","pilot_doctor","pilot_combatmedic","pilot_tactician"
    ],
    "Mixed": [
        "pilot_bookish", "pilot_cautious", "pilot_criminal", "pilot_dependable",
        "pilot_dishonest", "pilot_drunk", "pilot_reckless", "pilot_honest",
        "pilot_noble", "pilot_bushido", "pilot_zealot", "pilot_feral", "pilot_redline","pilot_archer","pilot_warhead",
        "pilot_eoptics","pilot_coptics","pilot_keepmoving","pilot_intimidating","pilot_adrenaline","pilot_boxer","pilot_taekwondo"
    ],
    "Negative": [
        "pilot_klutz", "pilot_nervous", "pilot_fragile", "pilot_apathetic",
        "pilot_lazyeye", "pilot_traumatic_injury", "pilot_nearsighted",
        "pilot_limitedvision", "pilot_conspicuous", "pilot_pretentious",
        "pilot_reject", "pilot_jinxed","pilot_glassjaw","pilot_tunnelvision","pilot_lazy","pilot_offbalance","pilot_inadequate","pilot_cowardly"
    ],
}

# Characteristics
characteristics = {
    "Eyes": ["hazel", "brown", "blue", "green", "heterochromatic"],
    "Handedness": ["right", "left", "ambidextrous"],
    "Blood Type": ["ab_positive", "a_negative", "o_positive", "a_positive", "ab_negative", "o_negative"],
    "Stature": ["above_average", "tall", "average", "short", "below_average"],
}

# Output folder for JSON files relative to the script's location
output_folder = os.path.join(script_directory, "PilotGeneration")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)
# Define the MechTech perks and their probabilities
mechtech_perks = ["pilot_novice_technician", "pilot_tech", "pilot_adv_technician", "pilot_master_technician"]
roll1_probability = 0.23  # 23% chance for Roll 1
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
    # Roll for MechTech perks (Roll 1)
    if random.random() < roll1_probability:
        # Roll 2 (if Roll 1 is true)
        roll2_probability = random.random()
        if roll2_probability < 0.60:
            perks["Positive"].append("pilot_novice_technician")
        elif roll2_probability < 0.90:
            perks["Positive"].append("pilot_tech")
        elif roll2_probability < 0.99:
            perks["Positive"].append("pilot_adv_technician")
        else:
            perks["Positive"].append("pilot_master_technician")


    # Minimum perks required for each category
    min_perks = {
        "Green": (1, 0, 0),
        "Regular": (1, 1, 0),
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
    if pilot_name in ["Apex", "Arclight", "Blockade", "Buckshot", "Kraken", "Mockingbird", "Ozone", "Paradise", "Showboat", "Squire", "Sumo", "Wildfire","Witness"]:
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
                f"bloodtype_{pilot_characteristics['Blood Type'].lower()}",
                f"stature_{pilot_characteristics['Stature'].lower()}",
            ]
        }
    }

    # Add the "pilot_" prefix only to perk tags
    traits = [trait.lower() for trait in pilot_perks["Positive"] + pilot_perks["Mixed"] + pilot_perks["Negative"]]
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
                # Check the generation of each file
                pilots_generation_time = os.path.getmtime(pilots_file_path)
                pilot_generation_time = os.path.getmtime(pilot_generation_file_path)

                if pilots_generation_time > pilot_generation_time:
                    print(f"Skipping {filename}: Pilots file is newer than PilotGeneration file.")
                    continue

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

                    # Merge the tags, ensuring there are no duplicates and preserving the prefixes
                    pilot_tags_merged = []

                    for tag in pilot_tags_new:
                        # Check if the tag is a characteristic or a perk, and add the correct prefix
                        if tag in faction_tags:
                            tag = f"name_{tag}"
                        elif tag in tag_exceptions:
                            tag = f"{tag}_{pilot_tags_existing[tag_exceptions.index(tag)]}"
                        elif tag not in pilot_tags_existing:
                            pilot_tags_merged.append(tag)

                    pilots_data["PilotTags"]["items"].extend(pilot_tags_merged)

                # Write the updated data back to the Pilots file
                with open(pilots_file_path, "w") as pilots_file:
                    json.dump(pilots_data, pilots_file, indent=4)

                print(f"PilotTags merged successfully for {filename}")
            else:
                print(f"Skipping {filename}: PilotGeneration file does not exist.")


# Call the function to merge PilotTags for all files
merge_pilot_tags_for_files(output_directory, output_folder)