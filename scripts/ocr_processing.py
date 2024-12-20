import os
import re
import cv2
import numpy as np
import pytesseract
import logging

# Setup logging
logging.basicConfig(filename='/home/harshavardhan/Documents/OCR_Project/logs/ocr_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directory paths
input_dir = '/home/harshavardhan/Documents/OCR_Project/output'
output_dir = '/home/harshavardhan/Documents/OCR_Project/output'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def preprocess_image(img_path):
    logging.info(f"Processing image: {img_path}")
    img = cv2.imread(img_path)
    if img is None:
        logging.error(f"Image not found or unable to read: {img_path}")
        raise FileNotFoundError(f"Image not found or unable to read: {img_path}")

    # Rescale the image
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove shadows and noise
    rgb_planes = cv2.split(img)
    result_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    img = cv2.merge(result_planes)

    # Apply dilation and erosion to remove noise
    img = cv2.dilate(img, np.ones((1, 1), np.uint8), iterations=1)
    img = cv2.erode(img, np.ones((1, 1), np.uint8), iterations=1)

    # Apply Gaussian blur and thresholding
    img = cv2.GaussianBlur(img, (1, 1), 0)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return img

def perform_ocr(img):
    logging.info("Performing OCR")
    return pytesseract.image_to_string(img, lang="tel")

def delete_images(directory):
    logging.info(f"Attempting to delete images in directory: {directory}")
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory, filename)
            logging.info(f"Attempting to delete file: {file_path}")
            try:
                os.remove(file_path)
                logging.info(f"Successfully deleted file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete {file_path}: {e}")

def process_images(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
            try:
                processed_img = preprocess_image(input_file_path)
                ocr_text = perform_ocr(processed_img)
                
                # Save the OCR result to a text file
                with open(output_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(ocr_text)
                logging.info(f'OCR completed for {filename}. Output saved to {output_file_path}')
            
            except Exception as e:
                logging.error(f'An error occurred for {filename}: {e}')

    # Delete all images after processing
    delete_images(input_dir)

# Execute the image processing
process_images(input_dir, output_dir)
