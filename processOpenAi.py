import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError(
        "API key not found. Make sure OPENAI_API_KEY is set in the .env file.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Define input and output folders
input_folder = 'input_texts'
output_folder = 'output_jsons'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load system prompt from prompt.txt
try:
    with open('prompt.txt', 'r', encoding='utf-8') as prompt_file:
        SYSTEM_PROMPT = prompt_file.read().strip()
except FileNotFoundError:
    raise FileNotFoundError(
        "The 'prompt.txt' file is missing. Please add it to the script's directory.")


def clean_content(content):
    """Strips leading and trailing code block markers from the content."""
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]  # Remove the leading ```json
    if content.endswith("```"):
        content = content[:-3]  # Remove the trailing ```
    return content.strip()


def process_file(file_path, output_path):
    """Reads a file, sends its content to the OpenAI API, and writes the cleaned response to a JSON file."""
    try:
        # Read the input file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Send content to OpenAI GPT-4 API with the system prompt
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ],
            temperature=0.0,
            max_tokens=4096,
        )

        # Extract and clean the "content" from the response
        # The latest library provides attribute access for the response object
        message_content = response.choices[0].message.content
        cleaned_content = clean_content(message_content)
        # Parse the cleaned content back into a dictionary
        parsed_content = json.loads(cleaned_content)

        # Save the cleaned response to the output file
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(parsed_content, outfile, indent=4)

        print(f"Processed and saved: {output_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def main():
    files = [f for f in os.listdir(input_folder) if os.path.isfile(
        os.path.join(input_folder, f))]

    if not files:
        print("No files found in the input folder.")
        return

    for idx, file_name in enumerate(files):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(
            output_folder, file_name.replace('.txt', '.json'))

        print(f"Processing file: {file_name}")
        process_file(input_path, output_path)

        # Check if there are more files to process
        if idx < len(files) - 1:
            next_file_confirm = input(
                f"Ready to delete {file_name} and proceed to the next file? (''/n): ").strip().lower()
            if next_file_confirm == '':
                os.remove(input_path)
            else:
                print(f"File {file_name} was not deleted.")
                return
        else:
            # For the last file, delete immediately after processing
            os.remove(input_path)
            print(f"Deleted input file: {input_path}")


if __name__ == "__main__":
    main()
