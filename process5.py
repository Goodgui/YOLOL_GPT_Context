import os
from bs4 import BeautifulSoup

# Input and output folders
input_folder = "processed4_html"
output_folder = "plaintext_files"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def convert_to_plaintext(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

        # Extract plain text
        plain_text = soup.get_text(separator="\n", strip=True)

        # Write the plain text to the output file
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(plain_text)

# Process all HTML files
for file_name in os.listdir(input_folder):
    if file_name.endswith(".html"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name.replace(".html", ".txt"))
        convert_to_plaintext(input_path, output_path)

print("Processing complete. Check the 'plaintext_files' folder.")
