import os
from bs4 import BeautifulSoup

# Input and output folders
input_folder = "processed2_html"
output_folder = "processed3_html"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def strip_styles_and_classes(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

        # Remove all style attributes
        for tag in soup.find_all(True):  # True finds all tags
            tag.attrs = {key: value for key, value in tag.attrs.items() if key == "id"}  # Keep only IDs

        # Write the cleaned HTML to the output file
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(str(soup))

# Process all HTML files
for file_name in os.listdir(input_folder):
    if file_name.endswith(".html"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        strip_styles_and_classes(input_path, output_path)

print("Processing complete. Check the 'processed3_html' folder.")
