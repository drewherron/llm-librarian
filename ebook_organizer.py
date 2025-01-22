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
    parser.add_argument("-i", "--instructions",
                       metavar="INSTRUCTION_FILE",
                       help="Path to a text file containing additional instructions for categorization")
    parser.add_argument("-b", "--batch-size",
                       type=int,
                       default=1,
                       help="Number of books to process in a single batch (default: 1)")
    return parser.parse_args()

def extract_year_from_date(date_str):
    """Extract year from common date formats found in ebooks.
    
    Args:
        date_str (str): Date string from metadata
        
    Returns:
        str: Year if found, empty string otherwise
    """
    if not date_str:
        return ""
        
    # Try different patterns
    year_patterns = [
        r'(20\d{2}|19\d{2})',  # 4-digit year (1900-2099)
        r'D:(20\d{2}|19\d{2})',  # PDF date format D:YYYY
        r'\d{2}/(20\d{2}|19\d{2})',  # MM/YYYY
        r'(20\d{2}|19\d{2})/\d{2}'   # YYYY/MM
    ]
    
    for pattern in year_patterns:
        matches = re.findall(pattern, date_str)
        if matches:
            return matches[0]
            
    return ""

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
                try:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
                except Exception as page_error:
                    print(f"Warning: Could not extract text from page {i} of {pdf_path}: {page_error}")

            # Extract metadata
            metadata = pdf.metadata or {}
            title = metadata.get("Title", "")
            author = metadata.get("Author", "")
            subject = metadata.get("Subject", "")
            creation_date = metadata.get("CreationDate", "")
            modification_date = metadata.get("ModDate", "")
            num_pages = len(pdf.pages)
            
            # Extract year
            year = extract_year_from_date(creation_date)
            if not year and modification_date:
                year = extract_year_from_date(modification_date)

        # Construct dictionary (metadata + extracted text)
        pdf_data = {
            "title": title,
            "author": author,
            "subject": subject,
            "creation_date": creation_date,
            "year": year,
            "num_pages": num_pages,
            "extracted_text": extracted_text[:1000]  # Limit text size
        }
        return pdf_data
    except Exception as e:
        print(f"Error extracting data from PDF file {pdf_path}: {e}")
        filename = os.path.basename(pdf_path)
        # Try to extract title and author from filename
        parts = filename.rsplit('.', 1)[0].split(' - ', 1)
        title = parts[0] if len(parts) > 0 else filename
        author = parts[1] if len(parts) > 1 else ""
        
        return {
            "title": title,
            "author": author,
            "year": "",
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

def determine_category(ebook_data, additional_instructions="", existing_categories=None):
    """
    Determine a category for the ebook based on its metadata.
    
    Args:
        ebook_data (dict): A dictionary containing ebook metadata.
        additional_instructions (str): Custom instructions for categorization.
        existing_categories (list): List of existing category directories.
        
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
    
    # Check for existing categories - prefer to reuse them for consistency
    if existing_categories:
        title = ebook_data.get('title', '').lower()
        text = ebook_data.get('extracted_text', '').lower()
        
        # Check if the book fits any existing category
        for cat in existing_categories:
            # For tech categories with language names
            if cat.startswith('Technology/') or cat.startswith('Programming/'):
                lang = cat.split('/')[-1].lower()
                if lang and (lang in title or lang in text):
                    return cat
            # Check for other categories
            elif '/' in cat:
                main_cat, sub_cat = cat.split('/', 1)
                sub_cat_lower = sub_cat.lower()
                if sub_cat_lower in title or sub_cat_lower in text:
                    return cat
    
    # Check if we have custom instructions for categorization
    if additional_instructions and "organize them into directories named after" in additional_instructions.lower():
        # This is likely programming language categorization
        if "programming language" in additional_instructions.lower():
            # Check specifically for programming books
            title = ebook_data.get('title', '').lower()
            text = ebook_data.get('extracted_text', '').lower()
            
            # Common programming languages
            languages = [
                'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'go', 
                'rust', 'swift', 'kotlin', 'php', 'typescript', 'perl', 
                'scala', 'haskell', 'r', 'matlab', 'sql', 'html', 'css'
            ]
            
            # Check for language-specific books
            for lang in languages:
                # Avoid false positives like "got" for "go"
                if lang == 'go' and ('got' in title or 'got' in text or 'going' in title or 'going' in text):
                    continue
                    
                if lang in title or lang in text:
                    # Check for web frameworks and technologies
                    web_frameworks = {
                        'django': 'Python', 'flask': 'Python', 'fastapi': 'Python',
                        'react': 'JavaScript', 'angular': 'JavaScript', 'vue': 'JavaScript',
                        'node': 'JavaScript', 'express': 'JavaScript',
                        'spring': 'Java', 'hibernate': 'Java',
                        'rails': 'Ruby', 'sinatra': 'Ruby',
                        'laravel': 'PHP', 'symfony': 'PHP'
                    }
                    
                    for framework, parent_lang in web_frameworks.items():
                        if framework in title.lower() or framework in text.lower():
                            # Structure as Technology/Language/Framework
                            return f"{parent_lang}/{framework.capitalize()}"
                    
                    # Structure as Technology/Language
                    return f"Technology/{lang.capitalize()}"
            
            # If it's programming but not language-specific
            if any(term in title or term in text for term in ['programming', 'code', 'developer', 'software']):
                return 'Technology/Programming'
                
            # Check for cloud platforms
            cloud_platforms = ['aws', 'amazon web services', 'azure', 'gcp', 'google cloud']
            for platform in cloud_platforms:
                if platform in title.lower() or platform in text.lower():
                    platform_name = {
                        'aws': 'AWS', 'amazon web services': 'AWS',
                        'azure': 'Azure', 
                        'gcp': 'GCP', 'google cloud': 'GCP'
                    }.get(platform, platform.upper())
                    return f"Technology/{platform_name}"
            
            # Skip non-programming books if instructed
            if "skip all other types of books" in additional_instructions.lower():
                return None
    
    # Standard categorization if no custom instructions or the book doesn't match custom criteria
    title = ebook_data.get('title', '').lower()
    text = ebook_data.get('extracted_text', '').lower()
    
    # Check for technology/programming books
    tech_keywords = ['programming', 'python', 'java', 'javascript', 'code', 'coding', 
                    'development', 'software', 'computer', 'web', 'database', 'data', 
                    'algorithm', 'cloud', 'network', 'security', 'hacking', 'linux', 
                    'windows', 'server', 'machine learning', 'ai', 'artificial intelligence']
    
    for keyword in tech_keywords:
        if keyword in title or keyword in text:
            # More specific tech categorization
            if 'python' in title or 'python' in text:
                return 'Technology/Python'
            elif 'javascript' in title or 'javascript' in text or 'js' in title:
                return 'Technology/JavaScript'
            elif 'java' in title or 'java' in text:
                return 'Technology/Java'
            elif 'web' in title or 'web' in text:
                return 'Technology/Web'
            else:
                return 'Technology'
    
    # Check for fiction books
    fiction_keywords = ['novel', 'fiction', 'story', 'stories', 'fantasy', 'adventure', 
                       'mystery', 'thriller', 'horror', 'romance', 'sci-fi', 'science fiction']
    
    for keyword in fiction_keywords:
        if keyword in title or keyword in text:
            # Subcategorize fiction
            if 'fantasy' in title or 'fantasy' in text:
                return 'Fiction/Fantasy'
            elif 'sci-fi' in title or 'science fiction' in text:
                return 'Fiction/Science Fiction'
            elif 'mystery' in title or 'mystery' in text or 'thriller' in title:
                return 'Fiction/Mystery'
            elif 'romance' in title or 'romance' in text:
                return 'Fiction/Romance'
            else:
                return 'Fiction'
    
    # Check for business books
    business_keywords = ['business', 'management', 'leadership', 'marketing', 'economics', 
                        'finance', 'investing', 'stock', 'entrepreneur', 'startup']
    
    for keyword in business_keywords:
        if keyword in title or keyword in text:
            return 'Business & Management'
    
    # Return default category if no match
    return category

def copy_ebook(ebook_path, ebook_info, output_dir, additional_instructions=""):
    """
    Renames the ebook and copies the file to the appropriate directory.

    Args:
        ebook_path (str): The current path of the ebook file.
        ebook_info (dict): A dictionary containing title, author.
        output_dir (str): The base output directory for organizing the ebooks.
        additional_instructions (str): Optional custom instructions for formatting.

    Returns:
        new_path (str): The path of the copied ebook file.
    """
    # Get the file extension
    file_ext = os.path.splitext(ebook_path)[1].lower()

    # Clean values for filesystem use
    author = ebook_info.get('author', 'Unknown Author').replace('/', '-')
    title = ebook_info.get('title', 'Untitled').replace('/', '-')
    year = ebook_info.get('year', 'Unknown').replace('/', '-')
    
    # Determine category
    category = ebook_info.get('category', 'Uncategorized')
    
    # Check for custom filename format in instructions
    if additional_instructions and "{title}" in additional_instructions and "{author}" in additional_instructions:
        if "format for filenames" in additional_instructions.lower():
            # Extract the format pattern
            lines = additional_instructions.split('\n')
            for line in lines:
                if "format for filenames" in line.lower():
                    # Get text within curly braces
                    parts = re.findall(r'\{(.*?)\}', line)
                    if parts and all(part in ['title', 'author', 'year'] for part in parts):
                        # Extract format pattern
                        if "{title} - {author} - {year}" in line:
                            new_filename = f"{title} - {author} - {year}{file_ext}"
                            break
                        elif "{year} - {title} - {author}" in line:
                            new_filename = f"{year} - {title} - {author}{file_ext}"
                            break
        else:
            new_filename = f"{title} - {author}{file_ext}"
    else:
        # Default filename format
        new_filename = f"{title} - {author}{file_ext}"

    # Create the new directory path based on category (handling hierarchical paths)
    new_dir = os.path.join(output_dir, category)
    os.makedirs(new_dir, exist_ok=True)

    # Create the new full path for the file
    new_path = os.path.join(new_dir, new_filename)

    # Copy the file
    shutil.copy2(ebook_path, new_path)

    return new_path

def process_batch(batch_paths, existing_categories, output_dir, additional_instructions=""):
    """Process a batch of ebooks together for efficiency.
    
    Args:
        batch_paths (list): List of paths to ebook files in this batch
        existing_categories (list): List of existing category directories
        output_dir (str): Output directory for organized files
        additional_instructions (str): Custom instructions for categorization
        
    Returns:
        list: List of dictionaries with organized ebook information
    """
    results = []
    
    # Process each book in the batch
    for ebook_path in batch_paths:
        print(f"Processing {os.path.basename(ebook_path)}...")
        
        # Extract ebook data
        ebook_data = extract_ebook_data(ebook_path)
        
        # Determine category
        category = determine_category(ebook_data, additional_instructions, existing_categories)
        
        # Skip this book if category is None (per instructions)
        if category is None:
            print("Skipping book (doesn't match criteria in instructions)")
            continue
        
        # Store category
        ebook_data['category'] = category
        
        print(f"Title: {ebook_data['title']}")
        print(f"Author: {ebook_data['author']}")
        print(f"Category: {category}")
        
        # Copy the ebook to the output directory
        new_path = copy_ebook(ebook_path, ebook_data, output_dir, additional_instructions)
        print(f"Copied to: {new_path}")
        print("-" * 40)
        
        # Add result to list
        results.append({
            'original_path': ebook_path,
            'new_path': new_path,
            'title': ebook_data['title'],
            'author': ebook_data['author'],
            'category': category
        })
        
        # Add to existing categories if it's a new category
        if category not in existing_categories:
            existing_categories.append(category)
            print(f"Added new category: {category}")
            
            # If it's a hierarchical category, also add the parent category
            if '/' in category:
                parent_category = category.split('/', 1)[0]
                if parent_category and parent_category not in existing_categories:
                    existing_categories.append(parent_category)
                    print(f"Added parent category: {parent_category}")
    
    return results

def organize_ebooks(ebook_directory, output_dir, additional_instructions="", batch_size=1):
    """
    Organize ebooks by copying them to appropriate directories.

    Args:
        ebook_directory (str): The directory containing ebook files and subdirectories.
        output_dir (str): The output directory for organized ebooks.
        additional_instructions (str): Custom instructions for categorization.
        batch_size (int): Number of ebooks to process in each batch.

    Returns:
        organized_files (list): List of organized file paths
    """
    # Get existing categories from output directory if it exists
    existing_categories = []
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        for root, dirs, _ in os.walk(output_dir):
            rel_path = os.path.relpath(root, output_dir)
            if rel_path != '.' and not rel_path.startswith('..'):
                existing_categories.append(rel_path)
        
        if existing_categories:
            print(f"Found {len(existing_categories)} existing category directories")
            print(f"Examples: {', '.join(existing_categories[:5])}" +
                 ("..." if len(existing_categories) > 5 else ""))
    
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

    # Process in batches if batch_size > 1
    if batch_size > 1:
        num_batches = (len(ebook_files) + batch_size - 1) // batch_size  # Ceiling division
        for i in range(0, len(ebook_files), batch_size):
            batch = ebook_files[i:i+batch_size]
            batch_num = i // batch_size + 1
            print(f"\nProcessing batch {batch_num} of {num_batches} ({len(batch)} books)")
            
            batch_results = process_batch(batch, existing_categories, output_dir, additional_instructions)
            organized_files.extend(batch_results)
    else:
        # Original single processing
        for ebook_path in ebook_files:
            print(f"Processing {ebook_path}...")
            
            # Get ebook data
            ebook_data = extract_ebook_data(ebook_path)
            
            # Determine category
            category = determine_category(ebook_data, additional_instructions, existing_categories)
            
            # Skip this book if category is None (per instructions)
            if category is None:
                print("Skipping book (doesn't match criteria in instructions)")
                continue
                
            ebook_data['category'] = category
            
            print(f"Title: {ebook_data['title']}")
            print(f"Author: {ebook_data['author']}")
            print(f"Category: {category}")
            
            # Copy the ebook to the output directory
            new_path = copy_ebook(ebook_path, ebook_data, output_dir, additional_instructions)
            print(f"Copied to: {new_path}")
            print("-" * 40)
            
            # Add to existing categories if it's a new category
            if category not in existing_categories:
                existing_categories.append(category)
                print(f"Added new category: {category}")
                
                # If it's a hierarchical category, also add the parent category
                if '/' in category:
                    parent_category = category.split('/', 1)[0]
                    if parent_category and parent_category not in existing_categories:
                        existing_categories.append(parent_category)
                        print(f"Added parent category: {parent_category}")
            
            organized_files.append({
                'original_path': ebook_path,
                'new_path': new_path,
                'title': ebook_data['title'],
                'author': ebook_data['author']
            })
        
    return organized_files

def main():
    args = get_args()
    
    # Check for instruction file
    additional_instructions = ""
    if args.instructions:
        try:
            with open(args.instructions, 'r') as f:
                additional_instructions = f.read().strip()
            print(f"Loaded additional instructions from {args.instructions}")
        except Exception as e:
            print(f"Error loading instructions file: {e}")
            return
    
    # Confirm with the user
    confirmation = input(f"This will categorize all ebooks (PDF, EPUB, MOBI, AZW3) in {args.ebook_dir} and all subdirectories, and copy them to {args.output_dir}\nAre you sure you want to proceed? (y/n)\n>> ")
    
    if confirmation.lower() == "y":
        batch_size = args.batch_size
        if batch_size > 1:
            print(f"Organizing ebooks in batches of {batch_size}...")
        else:
            print(f"Organizing ebooks...")
        organized_files = organize_ebooks(args.ebook_dir, args.output_dir, additional_instructions, batch_size)
        print(f"\nOrganized {len(organized_files)} ebook files to {args.output_dir}")
    else:
        print("\nAborting.\n")

if __name__ == "__main__":
    main()