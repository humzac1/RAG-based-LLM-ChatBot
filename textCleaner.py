import os
import re

def reduce_newlines(input_dir, output_dir):
    # Check if output directory exists; if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            # Construct full file path
            file_path = os.path.join(input_dir, filename)

            # Open and read the text file
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()

                # Use regex to replace multiple newlines with a single newline
                reduced_content = re.sub(r'\n\s*\n+', '\n\n', text_content)

                # Create a new text file for output
                output_file_path = os.path.join(output_dir, filename)
                with open(output_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(reduced_content)

                print(f"Processed {filename} and saved to {output_file_path}.")

input_directory = '' # Desired input directory
output_directory = '' # Desired output directory

reduce_newlines(input_directory, output_directory)
