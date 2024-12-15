import os
from bs4 import BeautifulSoup

# Directories
input_folder = "scraped_html"
output_folder = "processed1_html"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to extract the div and save it to a new file
def process_html_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")
        div = soup.find("div", class_="mw-parser-output")
        if div:
            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(str(div))

# Process all HTML files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".html"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        process_html_file(input_path, output_path)

print("Processing complete. Check the 'processed1_html' folder.")
