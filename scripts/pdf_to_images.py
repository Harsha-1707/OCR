import fitz  # PyMuPDF
import os

# Path to the PDF file and output directory for images
pdf_path = '/home/harshavardhan/Documents/OCR_Project/input/text.pdf'
output_dir = '/home/harshavardhan/Documents/OCR_Project/output'

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Iterate through the pages and save as images
for page_num in range(len(pdf_document)):
    page = pdf_document.load_page(page_num)
    pix = page.get_pixmap()
    image_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
    pix.save(image_path)
# 
print(f"Images saved in {output_dir}")
