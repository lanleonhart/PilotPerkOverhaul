import os
import json
import chardet

# List of tags to search for
search_tags = [
    "pilot_aurigan", "pilot_bloodspirit", "pilot_burrock", "pilot_circinus", "pilot_cloudcobra",
    "pilot_comstar", "pilot_coyote", "pilot_davion", "pilot_diamondshark", "pilot_firemandrill",
    "pilot_ghostbear", "pilot_goliathscorpion", "pilot_hellhorses", "pilot_icehellion",
    "pilot_illyria", "pilot_ives", "pilot_kurita", "pilot_liao", "pilot_lothian", "pilot_magistracy",
    "pilot_marian", "pilot_marik", "pilot_noble", "pilot_novacat", "pilot_outworld",
    "pilot_periphery", "pilot_smokejaguar", "pilot_snowraven", "pilot_solaris",
    "pilot_staradder", "pilot_steiner", "pilot_steelviper", "pilot_taurian", "pilot_tortuga",
    "pilot_valkyrate", "pilot_wolf", "pilot_worldofblake", "pilot_periphery"
]

# List of tags to ignore
ignore_tags = [
    "pilot_klutz", "pilot_nervous", "pilot_fragile", "pilot_apathetic",
    "pilot_lazyeye", "pilot_traumatic_injury", "pilot_nearsighted",
    "pilot_limitedvision", "pilot_conspicuous", "pilot_pretentious",
    "pilot_reject", "pilot_jinxed", "pilot_glassjaw", "pilot_tunnelvision", "pilot_lazy", "pilot_offbalance",
    "pilot_inadequate", "pilot_cowardly", "pilot_bookish", "pilot_cautious", "pilot_criminal", "pilot_dependable",
    "pilot_dishonest", "pilot_drunk", "pilot_reckless", "pilot_honest",
    "pilot_noble", "pilot_bushido", "pilot_zealot", "pilot_feral", "pilot_redline", "pilot_archer", "pilot_warhead",
    "pilot_eoptics", "pilot_coptics", "pilot_keepmoving", "pilot_intimidating", "pilot_adrenaline", "pilot_boxer",
    "pilot_taekwondo", "pilot_assassin", "pilot_athletic", "pilot_command", "pilot_ex-comstar", "pilot_lostech",
    "pilot_merchant", "pilot_military", "pilot_spacer", "pilot_technician", "pilot_resilient", "pilot_gunslinger",
    "pilot_deadeye", "pilot_gladiator", "pilot_officer", "pilot_brave", "pilot_inconspicuous", "pilot_calm", "pilot_lucky",
    "pilot_momentum", "pilot_tough", "pilot_anchored", "pilot_thrustvector", "pilot_doctor", "pilot_combatmedic",
    "pilot_tactician", "pilot_novice_technician", "pilot_tech", "pilot_adv_technician", "pilot_master_technician"
]

# Prefixes to ignore in unused tags
ignore_prefixes = ["name_", "stature_", "bloodtype_", "handedness_"]

# Output file path
output_file_path = "output.txt"

def detect_encoding(file_path):
    with open(file_path, 'rb') as raw_file:
        result = chardet.detect(raw_file.read())
    return result['encoding']

def search_tags_in_file(file_path):
    # Skip the file if it is 'revert.zip'
    if os.path.basename(file_path) == 'revert.zip':
        print(f"Ignoring file: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            # Rest of your code
    except UnicodeDecodeError:
        print(f"Error decoding file: {file_path}")
        return

if __name__ == "__main__":
    script_location = os.path.dirname(os.path.abspath(__file__))
    pilots_location = os.path.join(script_location)

    for filename in os.listdir(pilots_location):
        file_path = os.path.join(pilots_location, filename)
        search_tags_in_file(file_path)

# Output tags that are not in the search or ignore list
all_tags = set()
for root, dirs, files in os.walk(pilots_location):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                tags = data.get("PilotTags", {}).get("items", [])
                all_tags.update(tags)

unused_tags = all_tags - set(search_tags) - set(ignore_tags)
print(f"\nUnused Tags: {unused_tags}")

# Filter out tags with specified prefixes
filtered_unused_tags = {tag for tag in unused_tags if not any(tag.startswith(prefix) for prefix in ignore_prefixes)}
print(f"\nFiltered Unused Tags: {filtered_unused_tags}")

# Write the results to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write("Found Tags:\n")
    for tag in all_tags:
        output_file.write(f"{tag}\n")

    output_file.write("\nUnused Tags:\n")
    for tag in unused_tags:
        output_file.write(f"{tag}\n")

    output_file.write("\nFiltered Unused Tags:\n")
    for tag in filtered_unused_tags:
        output_file.write(f"{tag}\n")

print(f"\nResults saved to {output_file_path}")
