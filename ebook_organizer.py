#!/usr/bin/env python3

import os
import re
import argparse
import warnings
import pdfplumber
import ebooklib
from ebooklib import epub

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

def extract_epub_data(epub_path):
    """
    Extract metadata and text from an EPUB file.

    Args:
        epub_path (str): The path to the EPUB file.

    Returns:
        epub_data (dict): A dictionary containing title, author, and extracted text.
    """
    try:
        book = epub.read_epub(epub_path)
        
        # Extract metadata
        title = book.get_metadata('DC', 'title')
        title = title[0][0] if title else ""
        
        author = book.get_metadata('DC', 'creator')
        author = author[0][0] if author else ""
        
        # Extract text from the first few chapters/items
        extracted_text = ""
        count = 0
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content = item.get_content().decode('utf-8')
                # Simple HTML stripping
                content = re.sub('<[^<]+?>', ' ', content)
                extracted_text += content + "\n"
                count += 1
                if count >= 5:  # Limit to first 5 sections
                    break
        
        epub_data = {
            "title": title,
            "author": author,
            "extracted_text": extracted_text[:1000]  # Limit text size
        }
        
        return epub_data
    
    except Exception as e:
        print(f"Error extracting data from EPUB file {epub_path}: {e}")
        return {
            "title": "",
            "author": "",
            "extracted_text": f"Error processing file: {e}"
        }

def extract_ebook_data(ebook_path):
    """
    Extract data from an ebook file based on its extension.
    
    Args:
        ebook_path (str): The path to the ebook file.
        
    Returns:
        ebook_data (dict): A dictionary containing extracted data.
    """
    file_ext = os.path.splitext(ebook_path)[1].lower()
    
    if file_ext == '.pdf':
        return extract_pdf_data(ebook_path)
    elif file_ext == '.epub':
        return extract_epub_data(ebook_path)
    else:
        # Return basic data for unsupported formats
        return {
            "title": os.path.basename(ebook_path),
            "author": "Unknown",
            "extracted_text": f"Unsupported file format: {file_ext}"
        }

def main():
    args = get_args()
    print(f"Will organize ebooks from {args.ebook_dir} to {args.output_dir}")
    
    # Look for ebooks
    for root, _, files in os.walk(args.ebook_dir):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in ['.pdf', '.epub']:
                ebook_path = os.path.join(root, file)
                print(f"Processing {ebook_path}...")
                ebook_data = extract_ebook_data(ebook_path)
                print(f"Title: {ebook_data['title']}")
                print(f"Author: {ebook_data['author']}")
                print("-" * 40)

if __name__ == "__main__":
    main()