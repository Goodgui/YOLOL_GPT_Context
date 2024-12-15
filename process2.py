import os
from bs4 import BeautifulSoup

# Input and output folders
input_folder = "processed1_html"
output_folder = "processed2_html"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def process_html(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")
        
        # Locate the desired div
        main_div = soup.find("div", class_="mw-parser-output")
        if not main_div:
            print(f"Skipping {file_path} (No mw-parser-output found)")
            return

        # Remove unwanted sections (Contents, images, related content)
        for tag in main_div.select("div.toc, img, div#otherLang2, h2#Related_content, ul#related-content"):
            tag.decompose()

        # Replace <a> tags with their inner text
        for a_tag in main_div.find_all("a"):
            a_tag.replace_with(a_tag.get_text(strip=True))

        # Preserve table structure and write to the output file
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(str(main_div))

# Process all HTML files
for file_name in os.listdir(input_folder):
    if file_name.endswith(".html"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        process_html(input_path, output_path)

print("Processing complete. Check the 'processed1_html' folder.")
