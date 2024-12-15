import os
import json
import re

# Constants for customization
FIELDS = {
    "general": ["|size=", "|mass=", "|volume=", "|corrosionResistance=", "|primaryMaterial="],
    "io": ["|electricIn=", "|electricOut=", "|fuelIn=", "|fuelOut=", "|sockets=", "|modInterfaces="],
    "materials": [
        "|ajatite=", "|bastium=", "|charodium=", "|lukium=", "|ymrium=", "|aegisium=", "|vokarium="
    ],
    "meta": ["|name=", "|image=", "|type=", "|function=", "|caption="]
}


def normalize_size(size):
    """Normalize size format from '84×96×144 cm' to '84 x 96 x 144 cm'."""
    # Replace known variants of multiplication symbols with ' x '
    normalized_size = size.replace("×", " x ").replace("\u00d7", " x ").replace("\u00c3\u2014", " x ")
    # Ensure only a single ' x ' is inserted, and preserve the rest of the string
    return re.sub(r'\s*x\s*', ' x ', normalized_size).strip()


def parse_device(file_path):
    """Parse a single device file into a structured format."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    devices = []
    current_device = {"general": {}, "io": {},
                      "materials": {}, "meta": {}, "tiers": []}
    current_tier = {}

    for line in lines:
        line = line.strip()

        # Parse metadata and general information
        for field in FIELDS["meta"] + FIELDS["general"]:
            if line.startswith(field):
                key = field.strip("|=").lower()
                value = line.split('=')[1].strip()

                # Normalize specific fields
                if key == "size":
                    value = normalize_size(value)

                # Assign to appropriate section
                if field in FIELDS["meta"]:
                    current_device["meta"][key] = value
                else:
                    current_device["general"][key] = value

        # Parse material composition
        for field in FIELDS["materials"]:
            if line.startswith(field):
                key = field.strip("|=").lower()
                current_device["materials"][key] = line.split('=')[1].strip()

        # Handle tier-specific data
        if line.startswith("|name="):
            if current_tier:  # Save the previous tier
                current_device["tiers"].append(current_tier)
            current_tier = {"name": line.split('=')[1].strip()}

        # Add tier-specific general or material information
        if current_tier:
            for field in FIELDS["general"] + FIELDS["materials"]:
                if line.startswith(field):
                    key = field.strip("|=").lower()
                    value = line.split('=')[1].strip()
                    if field in FIELDS["general"]:
                        if key == "size":
                            value = normalize_size(value)
                        current_tier[key] = value
                    else:
                        current_tier.setdefault("composition", {})[key] = value

    # Finalize data
    if current_tier:
        current_device["tiers"].append(current_tier)
    if current_device:
        devices.append(current_device)

    # Reorganize the structure to match the desired output
    for device in devices:
        device["description"] = device["meta"].pop("caption", "")
        device["title"] = device["meta"].pop("name", "Unknown Device")
        device.pop("meta", None)  # Remove the meta placeholder if unused

    return devices


def process_txt_file(input_path, output_path):
    """Parse a single text file and save its output as JSON."""
    parsed_data = parse_device(input_path)
    with open(output_path, 'w') as json_file:
        json.dump(parsed_data, json_file, indent=4)


# Directories
input_folder = "(testinput"
output_folder = "(testoutput"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process all text files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".txt"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(
            output_folder, f"{os.path.splitext(file_name)[0]}.json")
        process_txt_file(input_path, output_path)

print("Processing complete. Check the 'processed_txt1' folder.")
