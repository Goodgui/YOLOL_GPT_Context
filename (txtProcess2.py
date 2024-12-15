import os
import json
import re


def parse_device(input_path):
    """Parse title and summary from a single text file."""
    title = None
    summary = None

    with open(input_path, 'r') as file:
        content = file.read()

        # Extract title (based on |name= or similar patterns)
        title_match = re.search(r'\|name=([\w\s-]*)', content)
        if title_match:
            title = title_match.group(1).strip()

        # Extract summary (based on <section begin=summary/> ... <section end=summary/>)
        summary_match = re.search(r'<section begin=summary/>(.*?)<section end=summary/>', content, re.S)
        if summary_match:
            summary = summary_match.group(1).strip()

    # Return parsed data
    return {
        "title": title or "Untitled",  # Default if no title is found
        "summary": summary or "No summary provided"  # Default if no summary is found
    }


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

print("Processing complete. Check the 'testoutput' folder.")
