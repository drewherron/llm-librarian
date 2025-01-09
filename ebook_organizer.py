#!/usr/bin/env python3

import os
import argparse
import warnings
import pdfplumber

# Suppress specific pdfplumber warnings
warnings.filterwarnings("ignore", message="CropBox missing from /Page, defaulting to MediaBox")

def get_args():
    parser = argparse.ArgumentParser(
        prog="python3 ebook_organizer.py",
        description="Organize a collection of ebook files.")
    parser.add_argument("ebook_dir",
                       help="Directory containing ebook files to organize")
    parser.add_argument("output_dir",
                       help="Directory where organized ebooks will be copied")
    return parser.parse_args()

def extract_pdf_data(pdf_path):
    """
    Extract metadata and text from the first few pages of a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        pdf_data (dict): A dictionary containing metadata and extracted text.
    """
    # Extract text from the first 5 pages
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages_to_read = min(5, len(pdf.pages))
            for i in range(num_pages_to_read):
                page = pdf.pages[i]
                extracted_text += page.extract_text() + "\n"

            # Extract metadata
            metadata = pdf.metadata
            title = metadata.get("Title", "")
            author = metadata.get("Author", "")
            subject = metadata.get("Subject", "")
            creation_date = metadata.get("CreationDate", "")
            num_pages = len(pdf.pages)

        # Construct dictionary (metadata + extracted text)
        pdf_data = {
            "title": title,
            "author": author,
            "subject": subject,
            "creation_date": creation_date,
            "num_pages": num_pages,
            "extracted_text": extracted_text[:1000]  # Limit text size
        }
        return pdf_data
    except Exception as e:
        print(f"Error extracting data from PDF file {pdf_path}: {e}")
        return {
            "title": "",
            "author": "",
            "extracted_text": f"Error processing file: {e}"
        }

def main():
    args = get_args()
    print(f"Will organize ebooks from {args.ebook_dir} to {args.output_dir}")
    
    # Example PDF extraction
    for root, _, files in os.walk(args.ebook_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                print(f"Processing {pdf_path}...")
                pdf_data = extract_pdf_data(pdf_path)
                print(f"Title: {pdf_data['title']}")
                print(f"Author: {pdf_data['author']}")
                print(f"Number of pages: {pdf_data.get('num_pages', 'Unknown')}")
                print("-" * 40)

if __name__ == "__main__":
    main()