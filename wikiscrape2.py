import requests
import os
from lxml import html
from time import sleep

# Path to the input file
input_file = "urls.txt"

# Directory to save the content files
output_dir = "scraped_html2"
os.makedirs(output_dir, exist_ok=True)

# Function to extract and save content
def scrape_and_save(url, title):
    try:
        response = requests.get(url+"&action=edit", timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML content using lxml
        tree = html.fromstring(response.content)

        # Extract the content using XPath
        textarea = tree.xpath('//*[(@id = "wpTextbox1")]')
        if textarea:
            content = textarea[0].text
        else:
            print(f"No content found in {url}")
            return

        # Save content to a file
        filename = f"{title}.txt"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Saved: {url} -> {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

# Read input file
with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Base URL
base_url = lines[0].strip()

# Process each title
for line in lines[1:]:
    title = line.strip().replace(" ", "_")
    if title:  # Skip empty lines
        full_url = f"{base_url}{title}"
        scrape_and_save(full_url, title)
        sleep(1)  # Add a 1-second delay between requests
