import os
from bs4 import BeautifulSoup

# Input and output folders
input_folder = "processed3_html"
output_folder = "processed4_html"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def remove_empty_and_single_element_tags(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

        # Iterate through all tags and remove empty ones or those with a single child
        for tag in soup.find_all(True):  # True finds all tags
            # If the tag is empty or contains only one non-empty child
            if not tag.get_text(strip=True) and not tag.find(True):
                tag.decompose()  # Remove empty tag
            elif len(tag.find_all(True, recursive=False)) == 1 and not tag.get_text(strip=True, separator=""):
                tag.unwrap()  # Remove the tag but keep its content

        # Write the cleaned HTML to the output file
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(str(soup))

# Process all HTML files
for file_name in os.listdir(input_folder):
    if file_name.endswith(".html"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        remove_empty_and_single_element_tags(input_path, output_path)

print("Processing complete. Check the 'processed4_html' folder.")
