#!/usr/bin/env python3

import os
import re
import sys
import shutil
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

def extract_mobi_azw3_data(ebook_path):
    """
    Basic extraction for MOBI and AZW3 files.
    Note: For robust MOBI/AZW3 parsing, additional libraries may be needed.
    
    Args:
        ebook_path (str): The path to the MOBI or AZW3 file.
        
    Returns:
        ebook_data (dict): A dictionary containing minimal information.
    """
    # For MOBI/AZW3, we'll just extract the filename as fallback data
    # In a production app, you'd use a dedicated library like mobi or KindleUnpack
    filename = os.path.basename(ebook_path)
    
    # Try to extract title/author from filename pattern like "Title - Author.mobi"
    parts = filename.rsplit('.', 1)[0].split(' - ', 1)
    
    title = parts[0] if len(parts) > 0 else "Unknown"
    author = parts[1] if len(parts) > 1 else "Unknown"
    
    ebook_data = {
        "title": title,
        "author": author,
        "extracted_text": f"Limited metadata extraction for {os.path.basename(ebook_path)}"
    }
    
    return ebook_data

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
    elif file_ext in ['.mobi', '.azw3']:
        return extract_mobi_azw3_data(ebook_path)
    else:
        # Return basic data for unsupported formats
        return {
            "title": os.path.basename(ebook_path),
            "author": "Unknown",
            "extracted_text": f"Unsupported file format: {file_ext}"
        }

def determine_category(ebook_data):
    """
    Determine a category for the ebook based on its metadata.
    
    Args:
        ebook_data (dict): A dictionary containing ebook metadata.
        
    Returns:
        category (str): The determined category.
    """
    # Default category
    category = 'Uncategorized'
    
    # List of standard categories
    categories = [
        "Fiction", "Non-Fiction", "History", "Philosophy", "Technology",
        "Science", "Biography", "Self-Help", "Fantasy", "Mystery", "Romance",
        "Horror", "Health & Wellness", "Travel", "Politics", "Economics",
        "Art & Design", "Religion & Spirituality", "Education", "Cooking",
        "Children's Books", "Poetry", "Drama", "Science Fiction", "Business & Management"
    ]
    
    # Simple categorization based on title and extracted text
    title = ebook_data.get('title', '').lower()
    text = ebook_data.get('extracted_text', '').lower()
    
    # Check for technology/programming books
    tech_keywords = ['programming', 'python', 'java', 'javascript', 'code', 'coding', 
                    'development', 'software', 'computer', 'web', 'database', 'data', 
                    'algorithm', 'cloud', 'network', 'security', 'hacking', 'linux', 
                    'windows', 'server', 'machine learning', 'ai', 'artificial intelligence']
    
    for keyword in tech_keywords:
        if keyword in title or keyword in text:
            return 'Technology'
    
    # Check for fiction books
    fiction_keywords = ['novel', 'fiction', 'story', 'stories', 'fantasy', 'adventure', 
                       'mystery', 'thriller', 'horror', 'romance', 'sci-fi', 'science fiction']
    
    for keyword in fiction_keywords:
        if keyword in title or keyword in text:
            return 'Fiction'
    
    # Check for business books
    business_keywords = ['business', 'management', 'leadership', 'marketing', 'economics', 
                        'finance', 'investing', 'stock', 'entrepreneur', 'startup']
    
    for keyword in business_keywords:
        if keyword in title or keyword in text:
            return 'Business & Management'
    
    # Return default category if no match
    return category

def copy_ebook(ebook_path, ebook_info, output_dir):
    """
    Renames the ebook and copies the file to the appropriate directory.

    Args:
        ebook_path (str): The current path of the ebook file.
        ebook_info (dict): A dictionary containing title, author.
        output_dir (str): The base output directory for organizing the ebooks.

    Returns:
        new_path (str): The path of the copied ebook file.
    """
    # Get the file extension
    file_ext = os.path.splitext(ebook_path)[1].lower()

    # Clean values for filesystem use
    author = ebook_info.get('author', 'Unknown Author').replace('/', '-')
    title = ebook_info.get('title', 'Untitled').replace('/', '-')
    
    # Determine category
    category = ebook_info.get('category', 'Uncategorized')
    
    # Create new filename
    new_filename = f"{title} - {author}{file_ext}"

    # Create the new directory path based on category
    new_dir = os.path.join(output_dir, category)
    os.makedirs(new_dir, exist_ok=True)

    # Create the new full path for the file
    new_path = os.path.join(new_dir, new_filename)

    # Copy the file
    shutil.copy2(ebook_path, new_path)

    return new_path

def organize_ebooks(ebook_directory, output_dir):
    """
    Organize ebooks by copying them to appropriate directories.

    Args:
        ebook_directory (str): The directory containing ebook files and subdirectories.
        output_dir (str): The output directory for organized ebooks.

    Returns:
        organized_files (list): List of organized file paths
    """
    organized_files = []

    # Recursively search for all ebook files
    ebook_files = []
    for root, _, files in os.walk(ebook_directory):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in ['.pdf', '.epub', '.mobi', '.azw3']:
                ebook_files.append(os.path.join(root, file))

    if len(ebook_files) == 0:
        print(f"No ebooks found in {ebook_directory}")
        return organized_files
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Organize each found ebook
    for ebook_path in ebook_files:
        print(f"Processing {ebook_path}...")
        
        # Get ebook data
        ebook_data = extract_ebook_data(ebook_path)
        
        # Determine category
        category = determine_category(ebook_data)
        ebook_data['category'] = category
        
        print(f"Title: {ebook_data['title']}")
        print(f"Author: {ebook_data['author']}")
        print(f"Category: {category}")
        
        # Copy the ebook to the output directory
        new_path = copy_ebook(ebook_path, ebook_data, output_dir)
        print(f"Copied to: {new_path}")
        print("-" * 40)
        
        organized_files.append({
            'original_path': ebook_path,
            'new_path': new_path,
            'title': ebook_data['title'],
            'author': ebook_data['author']
        })
        
    return organized_files

def main():
    args = get_args()
    
    # Confirm with the user
    confirmation = input(f"This will categorize all ebooks (PDF, EPUB, MOBI, AZW3) in {args.ebook_dir} and all subdirectories, and copy them to {args.output_dir}\nAre you sure you want to proceed? (y/n)\n>> ")
    
    if confirmation.lower() == "y":
        print(f"Organizing ebooks...")
        organized_files = organize_ebooks(args.ebook_dir, args.output_dir)
        print(f"\nOrganized {len(organized_files)} ebook files to {args.output_dir}")
    else:
        print("\nAborting.\n")

if __name__ == "__main__":
    main()