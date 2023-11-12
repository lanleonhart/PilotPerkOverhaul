import os
import json

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()

# Perk categories
perk_categories = {
      "Positive": [
        "pilot_assassin", "pilot_athletic", "pilot_command", "pilot_ex-comstar", "pilot_lostech", "pilot_merchant", "pilot_military", "pilot_spacer",
        "pilot_technician", "pilot_resilient", "pilot_gunslinger", "pilot_deadeye", "pilot_gladiator", "pilot_officer", "pilot_brave", "pilot_inconspicuous",
        "pilot_calm", "pilot_lucky","pilot_momentum","pilot_tough","pilot_anchored","pilot_thrustvector","pilot_doctor","pilot_combatmedic"
    ],
    "Mixed": [
        "pilot_bookish", "pilot_cautious", "pilot_criminal", "pilot_dependable",
        "pilot_dishonest", "pilot_drunk", "pilot_reckless", "pilot_honest",
        "pilot_noble", "pilot_bushido", "pilot_zealot", "pilot_feral", "pilot_redline","pilot_archer","pilot_warhead",
        "pilot_eoptics","pilot_coptics","pilot_keepmoving","pilot_intimidating"
    ],
    "Negative": [
        "pilot_klutz", "pilot_nervous", "pilot_fragile", "pilot_apathetic",
        "pilot_lazyeye", "pilot_traumatic_injury", "pilot_nearsighted",
        "pilot_limitedvision", "pilot_conspicuous", "pilot_pretentious",
        "pilot_reject", "pilot_jinxed","pilot_glassjaw"
    ],
    "Mechtech": ["pilot_novice_technician", "pilot_tech", "pilot_adv_technician", "pilot_master_technician"],
}

# Characteristics
characteristics = {
    "Eyes": ["eyes_heterochromatic", "eyes_brown", "eyes_blue", "eyes_green", "eyes_hazel"],
    "Handedness": ["handedness_right", "handedness_left", "handedness_ambidextrous"],
    "Blood Type": ["bloodtype_b_positive", "bloodtype_a_negative", "bloodtype_o_positive", "bloodtype_a_positive", "bloodtype_ab_negative", "bloodtype_ab_positive", "bloodtype_o_negative"],
    "Stature": ["stature_average", "stature_tall", "stature_above_average", "stature_short", "stature_below_average"],
}

# Faction Tags
faction_tags = [
    "pilot_aurigan", "pilot_bloodspirit", "pilot_burrock", "pilot_circinus", "pilot_cloudcobra",
    "pilot_comstar", "pilot_coyote", "pilot_davion", "pilot_diamondshark", "pilot_firemandrill",
    "pilot_ghostbear", "pilot_goliathscorpion", "pilot_hellshorses", "pilot_icehellion",
    "pilot_illyria", "pilot_ives", "pilot_kurita", "pilot_liao", "pilot_lothian", "pilot_magistracy",
    "pilot_marian", "pilot_marik", "pilot_noble", "pilot_novacat", "pilot_outworld",
    "pilot_periphery", "pilot_smokejaguar", "pilot_snowraven", "pilot_solaris",
    "pilot_staradder", "pilot_steiner", "pilot_steelviper", "pilot_taurian", "pilot_tortuga",
    "pilot_valkyrate", "pilot_wolf", "pilot_worldofblake"
]

# Define the directory where the JSON files are located
pilots_directory = os.path.join(script_dir, "..", "PilotPerkOverhaul", "Pilots")

# Initialize dictionaries to store counts
positive_perks = {perk: 0 for perk in perk_categories["Positive"]}
mixed_perks = {perk: 0 for perk in perk_categories["Mixed"]}
negative_perks = {perk: 0 for perk in perk_categories["Negative"]}
mechtech_perks = {perk: 0 for perk in perk_categories["Mechtech"]}
characteristic_perks = {char: {tag: 0 for tag in char_tags} for char, char_tags in characteristics.items()}
faction_tags_counts = {tag: 0 for tag in faction_tags}

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
                mechtech_perks[tag] += 1
            elif tag in faction_tags:
                faction_tags_counts[tag] += 1
            else:
                for char, char_tags in characteristics.items():
                    for char_tag in char_tags:
                        if tag.startswith(char_tag):
                            characteristic_perks[char][char_tag] += 1
                            break

# Process all pilot files
for filename in os.listdir(pilots_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(pilots_directory, filename)
        process_pilot_file(file_path)

# Get the total number of pilot JSON files in the directory
total_pilots = len([f for f in os.listdir(pilots_directory) if f.endswith(".json")])

# Sort the perks, characteristics, and faction tags by occurrence in descending order
sorted_positive_perks = sorted(positive_perks.items(), key=lambda x: x[1], reverse=True)
sorted_mixed_perks = sorted(mixed_perks.items(), key=lambda x: x[1], reverse=True)
sorted_negative_perks = sorted(negative_perks.items(), key=lambda x: x[1], reverse=True)
sorted_mechtech_perks = sorted(mechtech_perks.items(), key=lambda x: x[1], reverse=True)
sorted_characteristics = {char: sorted(char_tags.items(), key=lambda x: x[1], reverse=True) for char, char_tags in characteristic_perks.items()}
sorted_faction_tags = sorted(faction_tags_counts.items(), key=lambda x: x[1], reverse=True)

# Define the output file path
output_file_path = os.path.join(script_dir, 'roll_summary.txt')

# Open the output file for writing and use a context manager (with statement)
with open(output_file_path, "w") as output_file:
    output_file.write("-" * 30 + "\n")
    output_file.write("Positive Perks Breakdown (Highest Occurrence to Lowest):\n")
    output_file.write("-" * 30 + "\n")
    for perk, count in sorted_positive_perks:
        fraction = f"{count}/{total_pilots}"
        percentage = f"{(count / total_pilots * 100):.2f}%"
        output_file.write(f"{perk}: {fraction} ({percentage})\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("Mixed Perks Breakdown (Highest Occurrence to Lowest):\n")
    output_file.write("-" * 30 + "\n")
    for perk, count in sorted_mixed_perks:
        fraction = f"{count}/{total_pilots}"
        percentage = f"{(count / total_pilots * 100):.2f}%"
        output_file.write(f"{perk}: {fraction} ({percentage})\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("Negative Perks Breakdown (Highest Occurrence to Lowest):\n")
    output_file.write("-" * 30 + "\n")
    for perk, count in sorted_negative_perks:
        fraction = f"{count}/{total_pilots}"
        percentage = f"{(count / total_pilots * 100):.2f}%"
        output_file.write(f"{perk}: {fraction} ({percentage})\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("MechTech Perks Breakdown (Highest Occurrence to Lowest):\n")
    output_file.write("-" * 30 + "\n")
    for perk, count in sorted_mechtech_perks:
        fraction = f"{count}/{total_pilots}"
        percentage = f"{(count / total_pilots * 100):.2f}%"
        output_file.write(f"{perk}: {fraction} ({percentage})\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("Characteristic Perks Breakdown (Highest Occurrence to Lowest):\n")
    output_file.write("-" * 30 + "\n")
    for char, char_tags in sorted_characteristics.items():
        output_file.write(char + "\n")
        output_file.write("-" * 30 + "\n")
        for char_tag, count in char_tags:
            fraction = f"{count}/{total_pilots}"
            percentage = f"{(count / total_pilots * 100):.2f}%"
            output_file.write(f"{char_tag}: {fraction} ({percentage})\n")
        output_file.write("-" * 30 + "\n")

    output_file.write("-" * 30 + "\n")
    output_file.write("Faction Tags Breakdown (Highest Occurrence to Lowest):\n")
    output_file.write("-" * 30 + "\n")
    for tag, count in sorted_faction_tags:
        fraction = f"{count}/{total_pilots}"
        percentage = f"{(count / total_pilots * 100):.2f}%"
        output_file.write(f"{tag}: {fraction} ({percentage})\n")

print(f"Statistical data saved to {output_file_path}")
