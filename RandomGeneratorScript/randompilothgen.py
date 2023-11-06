import random
import os
from collections import Counter

# Data
pilots = {
    "Green": ["Bono", "FalkM", "Heysek", "Hollabaugh", "Jakes", "Korwes", "Miller", "Piazza", "Ryia", "Shvartz", "Slipais", "SwansonA", "Thomas", "Voyls", "Gibbs", "Godfrey", "Leone", "Liebenow", "Saada", "Sampson", "Woods", "Oliver", "Shields"],
    "Regular": ["Cochran", "Kaufman", "Loving", "Reichenbach", "Bixby", "Bozeman", "Brewer", "Brown", "Cleary", "Doukas", "Durand", "Eck", "Fielding", "Hording", "Hurtado", "Keane", "Lemos", "Mzik", "Nick"],
    "Veteran": ["Test9", "Archangel", "Reinke", "Alaniz", "Bemis", "Chang", "Chik", "Chung", "Coldfire", "Doochin", "Eckett", "Endorf", "FalkA", "Hardie", "Helterbran", "Hill", "Huxley"],
    "Elite": ["Apex", "Arclight", "Blockade", "Buckshot", "Kraken", "Mockingbird", "Ozone", "Paradise", "Showboat", "Squire", "Sumo", "Wildfire", "Witness"],
}

# Sort the pilots by category and name
sorted_pilots = [(category, name) for category, names in pilots.items() for name in sorted(names)]

perk_categories = {
    "Positive": [
        "pilot_assassin", "pilot_athletic", "pilot_command", "pilot_excomstar",
        "pilot_lostech", "pilot_merchant", "pilot_military", "pilot_spacer",
        "pilot_tech", "pilot_wealthy"
    ],
    "Mixed": [
        "pilot_bookish", "pilot_cautious", "pilot_criminal", "pilot_dependable",
        "pilot_dishonest", "pilot_drunk", "pilot_reckless", "pilot_honest",
        "pilot_noble", "pilot_bushido", "pilot_zealot", "pilot_feral", "pilot_redline"
    ],
    "Negative": [
        "pilot_klutz", "pilot_nervous", "pilot_fragile", "pilot_apathetic",
        "pilot_lazyeye", "pilot_traumatic_injury", "pilot_nearsighted",
        "pilot_limitedvision", "pilot_conspicious", "pilot_pretentious",
        "pilot_reject", "pilot_inconspicious", "pilot_calm", "pilot_jinxed"
    ],
}

characteristics = {
    "Eyes": ["Heterochromatic", "Brown", "Blue", "Green", "Hazel"],
    "Handedness": ["Left", "Ambidextrous", "Right"],
    "Blood Type": ["B+", "A-", "O+", "A+", "AB-", "AB+", "O-"],
    "Stature": ["Average", "Tall", "Above Average", "Short", "Below Average"],
}

# Initialize perk statistics
perk_counts = {"Positive": {}, "Mixed": {}, "Negative": {}}
for perk_type in perk_categories:
    for perk in perk_categories[perk_type]:
        perk_counts[perk_type][perk] = 0

all_perks = []

# Function to generate perks for a pilot
def generate_perks(pilot_category):
    perks = {
        "Positive": [],
        "Mixed": [],
        "Negative": [],
    }

    # Minimum perks required for each category
    min_perks = {
        "Green": (1, 0, 0),
        "Regular": (1, 0, 0),
        "Veteran": (1, 1, 0),
        "Elite": (2, 1, 0),
    }

    min_positive, min_mixed, min_negative = min_perks[pilot_category]

    # Roll for additional perks
    for _ in range(min_positive + (random.random() < 0.2)):
        perk = random.choice(perk_categories["Positive"])
        if perk not in perks["Positive"]:
            perks["Positive"].append(perk)
            perk_counts["Positive"][perk] += 1  # Update the perk count
            all_perks.append(perk)  # Update all perks list
    for _ in range(min_mixed + (random.random() < 0.3)):
        perk = random.choice(perk_categories["Mixed"])
        if perk not in perks["Mixed"]:
            perks["Mixed"].append(perk)
            perk_counts["Mixed"][perk] += 1  # Update the perk count
            all_perks.append(perk)  # Update all perks list
    for _ in range(min_negative + (random.random() < 0.4)):
        perk = random.choice(perk_categories["Negative"])
        if perk not in perks["Negative"]:
            perks["Negative"].append(perk)
            perk_counts["Negative"][perk] += 1  # Update the perk count
            all_perks.append(perk)  # Update all perks list

    # Randomly select characteristics
    pilot_characteristics = {
        "Eyes": random.choice(characteristics["Eyes"]),
        "Handedness": random.choice(characteristics["Handedness"]),
        "Blood Type": random.choice(characteristics["Blood Type"]),
        "Stature": random.choice(characteristics["Stature"]),
    }

    return perks, pilot_characteristics

# Output for individual pilot information
output = []

# Generate perks and characteristics for each pilot
for pilot_category, pilot_name in sorted_pilots:
    pilot_perks, pilot_characteristics = generate_perks(pilot_category)

    # Add pilot category information
    output.append(f"{pilot_name} ({pilot_category})")

    output.append("Characteristics")
    for char_type, char in pilot_characteristics.items():
        output.append(f"{char_type}: {char}")
    output.append("Traits")

    for perk_type, perk_list in pilot_perks.items():
        for perk in perk_list:
            output.append(f'{perk_type.capitalize()}: "{perk}"')

    # Add a separator line between each pilot's information
    output.append("---")

# Define the output file name with an absolute path
output_file = r"C:\Users\Aegis\OneDrive\Desktop\RandomGenScript\Random_Pilot_Generation_Summary.txt"

# Write output to the individual pilot information text document
try:
    with open(output_file, "w") as file:
        file.write("\n".join(output))
    print(f"Output has been saved to '{output_file}'.")
except FileNotFoundError as e:
    print(f"File not found error: {str(e)}")
except PermissionError as e:
    print(f"Permission error: {str(e)}")
except Exception as e:
    print(f"An error occurred while saving the output: {str(e)}")

# Create a list to store pilot category information
pilot_categories = {}

# Generate perks and characteristics for each pilot and categorize them
for pilot_category, pilot_name in sorted_pilots:
    pilot_perks, pilot_characteristics = generate_perks(pilot_category)
    if pilot_category not in pilot_categories:
        pilot_categories[pilot_category] = []

    # Add pilot category, name, perks, and characteristics to the list
    pilot_categories[pilot_category].append({
        "name": pilot_name,
        "perks": pilot_perks,
        "characteristics": pilot_characteristics,
    })

# Create an output file for the roll summary
roll_summary_output = []

# Function to calculate the percentage
def calculate_percentage(count, total):
    return (count / total) * 100 if total > 0 else 0

# Calculate the total number of pilots
total_pilots = sum(len(pilots) for pilots in pilot_categories.values())

# Output the pilot perks breakdown
roll_summary_output.append("Pilot Perks Breakdown:")
for category, pilots in pilot_categories.items():
    roll_summary_output.append(f"\nCategory: {category}\n")
    perk_count = {}

    # Count individual pilot perks
    for pilot in pilots:
        for perk_type, perk_list in pilot["perks"].items():
            for perk in perk_list:
                if perk not in perk_count:
                    perk_count[perk] = 0
                perk_count[perk] += 1

    # Sort perks by occurrence
    sorted_perks = sorted(perk_count.items(), key=lambda x: x[1], reverse=True)

    for perk, count in sorted_perks:
        percentage = calculate_percentage(count, total_pilots)
        roll_summary_output.append(f"{perk} assigned to {count} / {total_pilots} Pilots ({percentage:.2f}% Occurrence)")

# Output the characteristics breakdown
roll_summary_output.append("\nCharacteristic Traits Breakdown:")
characteristic_count = {}

# Count individual pilot characteristics
for pilots in pilot_categories.values():
    for pilot in pilots:
        for characteristic, value in pilot["characteristics"].items():
            if characteristic not in characteristic_count:
                characteristic_count[characteristic] = {}
            if value not in characteristic_count[characteristic]:
                characteristic_count[characteristic][value] = 0
            characteristic_count[characteristic][value] += 1

# Sort characteristics by occurrence
for characteristic, values in characteristic_count.items():
    roll_summary_output.append(f"\n{characteristic} Breakdown:")
    sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)
    for value, count in sorted_values:
        percentage = calculate_percentage(count, total_pilots)
        roll_summary_output.append(f"{value} assigned to {count} / {total_pilots} Pilots ({percentage:.2f}% Occurrence)")

# Define the output file name for the roll summary with an absolute path
roll_summary_output_file = r"C:\Users\Aegis\OneDrive\Desktop\RandomGenScript\roll_summary_overview.txt"

# Write output to the roll summary text document
try:
    with open(roll_summary_output_file, "w") as file:
        file.write("\n".join(roll_summary_output))
    print(f"Roll summary has been saved to '{roll_summary_output_file}'.")
except FileNotFoundError as e:
    print(f"File not found error: {str(e)}")
except PermissionError as e:
    print(f"Permission error: {str(e)}")
except Exception as e:
    print(f"An error occurred while saving the roll summary: {str(e)}")

# Output all possible perks breakdown
all_perks_count = Counter(all_perks)

all_perks_output = []

# Sort all perks by type and occurrence
for perk_type in perk_categories:
    all_perks_output.append(f"{perk_type.capitalize()} Perk List")
    for perk in perk_categories[perk_type]:
        count = all_perks_count[perk]
        percentage = calculate_percentage(count, total_pilots)
        all_perks_output.append(f"{perk}\t\t\t\t\t{count} / {total_pilots} Pilot(s)\t{percentage:.2f}% Occurrence")

# Define the output file name for all perks breakdown with an absolute path
all_perks_output_file = r"C:\Users\Aegis\OneDrive\Desktop\RandomGenScript\all_perks_breakdown.txt"

# Write output to the all perks breakdown text document
try:
    with open(all_perks_output_file, "w") as file:
        file.write("\n".join(all_perks_output))
    print(f"All perks breakdown has been saved to '{all_perks_output_file}'.")
except FileNotFoundError as e:
    print(f"File not found error: {str(e)}")
except PermissionError as e:
    print(f"Permission error: {str(e)}")
except Exception as e:
    print(f"An error occurred while saving the all perks breakdown: {str(e)}")
