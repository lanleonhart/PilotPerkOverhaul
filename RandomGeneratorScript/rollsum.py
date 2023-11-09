import os
import json

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

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
    "Mechtech":["pilot_novice_technician","pilot_tech","pilot_adv_technician","pilot_master_technician"],
}

# Characteristics
characteristics = {
    "Eyes": ["eyes_heterochromatic", "eyes_brown", "eyes_blue", "eyes_green", "eyes_hazel"],
    "Handedness": ["handedness_right", "handedness_left", "handedness_ambidextrous"],
    "Blood Type": ["bloodtype_b_positive", "bloodtype_a_negative", "bloodtype_o_positive", "bloodtype_a_positive", "bloodtype_ab_negative", "bloodtype_ab_positive", "bloodtype_o_negative"],
    "Stature": ["stature_average", "stature_tall", "stature_above_average", "stature_short", "stature_below_average"],
}

# Define the directory where the JSON files are located
pilots_directory = os.path.join(script_dir, "..", "PilotPerkOverhaul", "Pilots")

# Initialize dictionaries to store counts
positive_perks = {perk: 0 for perk in perk_categories["Positive"]}
mixed_perks = {perk: 0 for perk in perk_categories["Mixed"]}
negative_perks = {perk: 0 for perk in perk_categories["Negative"]}
mechtech_perks = {perk: 0 for perk in perk_categories["Mechtech"]}
characteristic_perks = {char: {tag: 0 for tag in char_tags} for char, char_tags in characteristics.items()}

# Function to process a pilot JSON file
def process_pilot_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        tags = data.get("PilotTags", {}).get("items", [])

        for tag in tags:
            if tag in positive_perks:
                positive_perks[tag] += 1
            elif tag in mixed_perks:
                mixed_perks[tag] += 1
            elif tag in negative_perks:
                negative_perks[tag] += 1
            elif tag in mechtech_perks:
                mechtech_perks[tag] += 1  # Corrected variable name
            else:
                for char, char_tags in characteristics.items():
                    for char_tag in char_tags:
                        if tag.startswith(char_tag):
                            characteristic_perks[char][char_tag] += 1
                            break

# Define the output file path
output_file_path = os.path.join(script_dir, 'roll_summary.txt')

# Process all pilot files
for filename in os.listdir(pilots_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(pilots_directory, filename)
        process_pilot_file(file_path)

# Open the output file for writing
with open(output_file_path, "w") as output_file:
    output_file.write("-" * 30 + "\n")
    output_file.write("Positive Perks Breakdown:\n")
    output_file.write("-" * 30 + "\n")
    for perk, count in positive_perks.items():
        output_file.write(f"{perk}: {count}\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("Mixed Perks Breakdown:\n")
    output_file.write("-" * 30 + "\n")
    for perk, count in mixed_perks.items():
        output_file.write(f"{perk}: {count}\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("Negative Perks Breakdown:\n")
    output_file.write("-" * 30 + "\n")
    for perk, count in negative_perks.items():
        output_file.write(f"{perk}: {count}\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("MechTech Perks Breakdown:\n")
    output_file.write("-" * 30 + "\n")
    for perk, count in mechtech_perks.items():  # Corrected variable name
        output_file.write(f"{perk}: {count}\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("Characteristic Perks Breakdown:\n")
    output_file.write("-" * 30 + "\n")
    for char, char_tags in characteristics.items():
        output_file.write(char + "\n")
        output_file.write("-" * 30 + "\n")
        for char_tag in char_tags:
            if char_tag in characteristic_perks[char]:
                output_file.write(f"{char_tag}: {characteristic_perks[char][char_tag]}\n")
        output_file.write("-" * 30 + "\n")

print(f"Statistical data saved to {output_file_path}")