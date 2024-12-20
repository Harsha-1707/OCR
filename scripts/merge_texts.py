import os
import re

# Define the path to the original PDF
pdf_path = '/home/harshavardhan/Documents/OCR_Project/input/text.pdf'  # Update this to match your actual PDF path

# Define the output path where text files are stored
output_path = '/home/harshavardhan/Documents/OCR_Project/output'

# Extract the PDF file name (without extension) to use as the merged file name
pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
merged_file_name = f"{pdf_name}_merged_output.txt"
merged_file_path = os.path.join(output_path, merged_file_name)

# Function to extract page number from the filename
def extract_page_number(file_name):
    match = re.search(r'page_(\d+)', file_name)
    return int(match.group(1)) if match else float('inf')

try:
    # Merge all text files into one in the correct order
    with open(merged_file_path, 'w', encoding='utf-8') as merged_file:
        text_files = [f for f in os.listdir(output_path) if f.endswith('.txt')]
        if not text_files:
            raise FileNotFoundError("No text files found in the specified directory.")

        for file_name in sorted(text_files, key=extract_page_number):
            page_number = extract_page_number(file_name)
            file_path = os.path.join(output_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Write the page number header
                    merged_file.write(f"\n--- Page {page_number} ---\n")
                    merged_file.write(content)
                    merged_file.write('\n')  # Add a newline after each file's content
            except Exception as e:
                print(f"Error reading {file_name}: {e}")

    print(f"All text files have been merged into {merged_file_path}")

    # Delete the individual text files after merging
    for file_name in text_files:
        file_path = os.path.join(output_path, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_name}")
        except Exception as e:
            print(f"Error deleting {file_name}: {e}")

    # Optionally, open the merged file in a text editor for manual editing
    os.system(f"gedit {merged_file_path}")  # Use 'gedit' or another text editor available on Pop!_OS

except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")
except PermissionError as e:
    print(f"PermissionError: {e}")
except OSError as e:
    print(f"OSError: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
