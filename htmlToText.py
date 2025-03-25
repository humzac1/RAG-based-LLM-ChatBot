import os
from bs4 import BeautifulSoup

def convert_html_to_text(input_dir, output_dir):
    # Check if output directory exists; if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".html") or filename.endswith(".htm"):
            # Construct full file path
            file_path = os.path.join(input_dir, filename)

            # Open and read the HTML file
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

                # Parse HTML content using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extract text from the parsed HTML
                text_content = soup.get_text()

                # Create a new text file for output
                output_file_path = os.path.join(output_dir, filename.replace('.html', '.txt').replace('.htm', '.txt'))
                with open(output_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text_content)

                print(f"Converted {filename} to text.")

# Example usage
input_directory = '' # desired input directory
output_directory = '' # desired output directory
convert_html_to_text(input_directory, output_directory)
