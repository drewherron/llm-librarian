#!/usr/bin/env python3

import os
import re
import json
import sys
import shutil
import argparse
import warnings
import pdfplumber
import ebooklib
from ebooklib import epub
from langchain_openai import OpenAI
from langchain_community.document_loaders import PDFPlumberLoader

# Suppress specific pdfplumber warnings
warnings.filterwarnings("ignore", message="CropBox missing from /Page, defaulting to MediaBox")

def get_args():
    parser = argparse.ArgumentParser(
        prog="python3 ebook_organizer.py",
        description="Organize a collection of ebook files (PDF, EPUB, MOBI, AZW3) using an LLM.")
    parser.add_argument("ebook_dir",
                       help="Directory containing ebook files to organize")
    parser.add_argument("output_dir",
                       help="Directory where organized ebooks will be copied")
    parser.add_argument("-i", "--instructions",
                       metavar="INSTRUCTION_FILE",
                       help="Path to a text file containing additional instructions for the LLM")
    parser.add_argument("-b", "--batch-size",
                       type=int,
                       default=1,
                       help="Number of books to process in a single LLM request (default: 1)")
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
        pdf_data (dict): A dictionary containing title, author, subject, keywords, creation date, modification date, producer, creator, number of pages, and extracted text.
    """
    # Load the PDF using PDFPlumberLoader
    loader = PDFPlumberLoader(pdf_path)
    documents = loader.load()

    # Extract text from the first 5 pages
    num_pages_to_read = 5
    extracted_text = ""
    for page in documents[:num_pages_to_read]:
        extracted_text += page.page_content + "\n"

    # Extract metadata
    with pdfplumber.open(pdf_path) as pdf:
        metadata = pdf.metadata
        title = metadata.get("Title", "")
        author = metadata.get("Author", "")
        subject = metadata.get("Subject", "")
        keywords = metadata.get("Keywords", "")
        creation_date = metadata.get("CreationDate", "")
        modification_date = metadata.get("ModDate", "")
        producer = metadata.get("Producer", "")
        creator = metadata.get("Creator", "")
        num_pages = len(pdf.pages)

    # Construct dictionary (metadata + extracted text)
    pdf_data = {
        "title": title,
        "author": author,
        "subject": subject,
        "keywords": keywords,
        "creation_date": creation_date,
        "modification_date": modification_date,
        "producer": producer,
        "creator": creator,
        "num_pages": num_pages,
        "extracted_text": extracted_text[:1000]
    }

    return pdf_data

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
                # Simple HTML stripping (a more robust solution would use BeautifulSoup)
                content = re.sub('<[^<]+?>', ' ', content)
                extracted_text += content + "\n"
                count += 1
                if count >= 5:  # Limit to first 5 sections
                    break

        epub_data = {
            "title": title,
            "author": author,
            "extracted_text": extracted_text[:1000]
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

def generate_ebook_dict(ebook_path, categories, additional_instructions="", use_default_categories=True, existing_categories=None):
    """
    Generate a dictionary with title, author, summary, and category for one ebook using an LLM.

    Args:
        ebook_path (str): The path to the ebook file.
        categories (list): A list of categories to use for classification.

    Returns:
        ebook_info (dict): A dictionary containing title, author, summary, and category.
    """
    # Extract the ebook data
    ebook_data = extract_ebook_data(ebook_path)

    # Define the base prompt
    llm_prompt = (
        f"The following text and metadata has been extracted from an ebook. Please complete the following tasks:\n\n"
        f"1. Suggest a suitable title for the document based on the metadata and extracted text.\n"
        f"2. Look for the author in the metadata and extracted text, limit to ONE name if multiple are found, or state 'Unknown' if nothing is found.\n"
        f"3. Identify the publication year if available, or estimate it based on content. Use the format YYYY. If unknown, use 'Unknown'.\n"
        f"4. Attempt to provide a summary of the entire book, not just the extracted text.\n"
    )

    # Add categorization instructions based on whether we're using default categories
    if use_default_categories:
        llm_prompt += (
            f"5. Categorize the document, preferably using a hierarchical directory structure with a '/' separator. \n"
            f"For example: 'Technology/Python', 'Technology/JavaScript', 'Fiction/Science Fiction', etc.\n"
            f"This creates a more organized structure with general categories and specific subcategories.\n"
            f"Here are some example main categories for guidance: {', '.join(categories)}.\n"
            f"You can use these examples or create more specific or appropriate categories.\n\n"
        )
    else:
        if existing_categories and len(existing_categories) > 0:
            llm_prompt += (
                f"5. Determine a suitable category based on the instructions below. \n"
                f"Preferably use a hierarchical structure with '/' separator, like 'Technology/Python' or 'Fiction/SciFi'.\n"
                f"If appropriate, choose from or extend these EXISTING categories: {', '.join(existing_categories)}.\n"
                f"Otherwise, create a new category that follows the instructions.\n\n"
            )
        else:
            llm_prompt += (
                f"5. Determine a suitable category based on the instructions below.\n"
                f"Preferably use a hierarchical structure with '/' separator, like 'Technology/Python'.\n\n"
            )

    # Add any additional instructions
    if additional_instructions:
        llm_prompt += f"Additional instructions (these override previous instructions if there are conflicts):\n{additional_instructions}\n\n"

    llm_prompt += (
        f"Please provide the output in the following structured format:\n"
        f"Title: <Title>\n"
        f"Author: <Author>\n"
        f"Year: <Year>\n"
        f"Summary: <Summary>\n"
        f"Category: <Category>\n\n"
        f"Here is the ebook data:\n"
        f"Title: {ebook_data.get('title', '')}\n"
        f"Author: {ebook_data.get('author', '')}\n"
        f"Creation Date: {ebook_data.get('creation_date', '')}\n\n"
        f"Extracted Text:\n{ebook_data.get('extracted_text', '')}\n"
    )

    # Use the LLM
    llm = OpenAI()
    response = llm.invoke(llm_prompt)

    print(f"LLM response: {response}\n")

    # Extract the LLM response
    lines = response.splitlines()

    # Check for filename format instruction in the response
    filename_format = None
    for line in lines:
        if line.startswith("Filename:") or line.startswith("Format:"):
            filename_format = line.split(":", 1)[1].strip()
    title, author, summary, category = "", "", "", ""

    for line in lines:
        if line.startswith("Title:"):
            title = line[len("Title:"):].strip()
        elif line.startswith("Author:"):
            author = line[len("Author:"):].strip()
        elif line.startswith("Year:"):
            year = line[len("Year:"):].strip()
        elif line.startswith("Summary:"):
            summary = line[len("Summary:"):].strip()
        elif line.startswith("Category:"):
            category = line[len("Category:"):].strip()

    print(f"title: {title}")
    print(f"author: {author}")
    print(f"year: {year if 'year' in locals() else 'Unknown'}")
    print(f"summary: {summary}")
    print(f"category: {category}")

    # Create the final ebook_info dictionary
    ebook_info = {
        'title': title or ebook_data.get('title', ''),
        'author': author or ebook_data.get('author', ''),
        'year': year if 'year' in locals() else 'Unknown',
        'summary': summary,
        'category': category,
        'original_path': ebook_path
    }

    # Add filename format if specified
    if filename_format:
        ebook_info['filename_format'] = filename_format

    return ebook_info

def process_batch(ebook_paths, categories, additional_instructions="", use_default_categories=True, existing_categories=None, max_retries=1):
    """
    Process a batch of ebooks with a single LLM call to improve token efficiency.
    
    Args:
        ebook_paths (list): List of paths to ebook files to process
        categories (list): A list of categories to use for classification
        additional_instructions (str): Custom instructions for categorization
        use_default_categories (bool): Whether to use default categories or custom ones
        existing_categories (list): List of existing category directories
        
    Returns:
        list: List of dictionaries with processed ebook information
    """
    # Extract data for all ebooks in the batch
    ebooks_data = []
    for path in ebook_paths:
        ebooks_data.append({
            'path': path,
            'data': extract_ebook_data(path)
        })
    
    # Create a single prompt for all ebooks
    llm_prompt = (
        f"I will provide you with data from {len(ebook_paths)} ebooks. Your task is to analyze each ebook and provide structured information.\n\n"
        f"For each book, you must:\n"
        f"1. Identify a suitable title based on the metadata and text\n"
        f"2. Identify ONE author name, or state 'Unknown' if not found\n"
        f"3. Identify the publication year (YYYY format) or estimate it, or use 'Unknown'\n"
        f"4. Write a concise summary of the book\n"
    )
    
    # Add categorization instructions
    if use_default_categories:
        llm_prompt += (
            f"5. Categorize each document, preferably using a hierarchical directory structure with a '/' separator\n"
            f"For example: 'Technology/Python', 'Technology/JavaScript', 'Fiction/Science Fiction', etc.\n"
            f"This creates a more organized structure with general categories and specific subcategories.\n"
            f"Example main categories: {', '.join(categories[:10])}...\n"
            f"You can use these examples or create more specific categories.\n\n"
        )
    else:
        if existing_categories and len(existing_categories) > 0:
            llm_prompt += (
                f"5. Determine a suitable category based on the instructions below.\n" 
                f"Preferably use a hierarchical structure with '/' separator, like 'Technology/Python'\n"
                f"If appropriate, choose from or extend these EXISTING categories: {', '.join(existing_categories[:10])}...\n"
                f"Otherwise, create a new category that follows the instructions.\n\n"
            )
        else:
            llm_prompt += (
                f"5. Determine a suitable category based on the instructions below.\n"
                f"Preferably use a hierarchical structure with '/' separator, like 'Technology/Python'.\n\n"
            )
    
    # Add any additional instructions
    if additional_instructions:
        llm_prompt += f"Additional instructions (these override previous instructions if there are conflicts):\n{additional_instructions}\n\n"
    
    # Format for responses - making it very explicit and structured
    llm_prompt += (
        f"For each book, you MUST respond using EXACTLY this format with no deviations:\n"
        f"---BOOK 1 START---\n"
        f"Title: The exact book title\n"
        f"Author: Author name\n"
        f"Year: Publication year (YYYY)\n"
        f"Summary: A summary of the book\n"
        f"Category: The category (preferably with hierarchy like Technology/Python)\n"
        f"---BOOK 1 END---\n\n"
        f"---BOOK 2 START---\n"
        f"Title: The exact book title\n"
        f"Author: Author name\n"
        f"Year: Publication year (YYYY)\n"
        f"Summary: A summary of the book\n"
        f"Category: The category (preferably with hierarchy like Technology/Python)\n"
        f"---BOOK 2 END---\n\n"
        f"And so on for each book. The number in the START and END tags MUST match the book number.\n"
        f"It's critical that you maintain this EXACT format for parsing.\n\n"
    )
    
    # Add data for each ebook
    for i, ebook in enumerate(ebooks_data, 1):
        data = ebook['data']
        llm_prompt += (
            f"EBOOK {i} DATA:\n"
            f"File: {os.path.basename(ebook['path'])}\n"
            f"Title: {data.get('title', '')}\n"
            f"Author: {data.get('author', '')}\n"
            f"Creation Date: {data.get('creation_date', '')}\n\n"
            f"Extracted Text:\n{data.get('extracted_text', '')}\n\n"
            f"------------------\n\n"
        )
    
    # Use the LLM
    llm = OpenAI()
    response = llm.invoke(llm_prompt)
    
    print(f"Processed batch of {len(ebook_paths)} books with a single LLM call\n")
    
    # Parse the responses
    # Try a more flexible pattern that looks for book sections
    book_sections = re.findall(r'---BOOK \d+ START---(.*?)---BOOK \d+ END---', response, re.DOTALL)
    
    # If parsing the batch response fails, fall back to processing books individually
    if len(book_sections) == 0:
        print("Batch processing response format not recognized. Falling back to individual processing.")
        results = []
        for path in ebook_paths:
            print(f"Processing {os.path.basename(path)} individually...")
            book_info = generate_ebook_dict(path, categories, additional_instructions, 
                                          use_default_categories, existing_categories)
            results.append(book_info)
        return results
    
    results = []
    
    # Match responses to the original ebook paths
    for i, section in enumerate(book_sections):
        if i >= len(ebook_paths):
            break
            
        # Initialize with default values
        ebook_info = {
            'title': '',
            'author': 'Unknown',
            'year': 'Unknown',
            'summary': '',
            'category': 'Uncategorized',
            'original_path': ebook_paths[i]
        }
        
        # Parse the section
        lines = section.strip().split('\n')
        for line in lines:
            if line.startswith("Title:"):
                ebook_info['title'] = line[len("Title:"):].strip() or os.path.basename(ebook_paths[i])
            elif line.startswith("Author:"):
                ebook_info['author'] = line[len("Author:"):].strip() or 'Unknown'
            elif line.startswith("Year:"):
                ebook_info['year'] = line[len("Year:"):].strip() or 'Unknown'
            elif line.startswith("Summary:"):
                ebook_info['summary'] = line[len("Summary:"):].strip()
            elif line.startswith("Category:"):
                ebook_info['category'] = line[len("Category:"):].strip() or 'Uncategorized'
            elif line.startswith("Filename:") or line.startswith("Format:"):
                ebook_info['filename_format'] = line.split(":", 1)[1].strip()
        
        # Use original data as fallback for missing fields
        original_data = ebooks_data[i]['data']
        if not ebook_info['title']:
            ebook_info['title'] = original_data.get('title', '') or os.path.basename(ebook_paths[i])
        if ebook_info['author'] == 'Unknown' and original_data.get('author'):
            ebook_info['author'] = original_data.get('author')
            
        results.append(ebook_info)
        
    # Handle case where we got fewer responses than books
    for i in range(len(book_sections), len(ebook_paths)):
        print(f"Warning: No LLM response for book {i+1}, using metadata only")
        original_data = ebooks_data[i]['data']
        ebook_info = {
            'title': original_data.get('title', '') or os.path.basename(ebook_paths[i]),
            'author': original_data.get('author', '') or 'Unknown',
            'year': 'Unknown',
            'summary': 'No summary available',
            'category': 'Uncategorized',
            'original_path': ebook_paths[i]
        }
        results.append(ebook_info)
    
    return results

def copy_ebook(ebook_path, ebook_info, output_dir):
    """
    Renames the ebook and copies the file to the directory corresponding to its category.

    Args:
        ebook_path (str): The current path of the ebook file.
        ebook_info (dict): A dictionary containing title, author, summary, and category.
        output_dir (str): The base output directory for organizing the ebooks.

    Returns:
        new_path (str): The path of the copied ebook file.
    """
    # Get the file extension
    file_ext = os.path.splitext(ebook_path)[1].lower()

    # Clean values for filesystem use
    author = ebook_info.get('author', 'Unknown Author').replace('/', '-')
    title = ebook_info.get('title', 'Untitled').replace('/', '-')
    year = ebook_info.get('year', 'Unknown').replace('/', '-')
    
    # For category, we keep the slashes for hierarchical paths, but clean other special chars
    category = ebook_info.get('category', 'Uncategorized').replace(':', '-').replace('\\', '-')

    # Check if the filename format is specified in the book info (custom from instructions)
    if ebook_info.get('filename_format'):
        filename_format = ebook_info.get('filename_format')
        # Replace placeholders with actual values
        new_filename = filename_format
        new_filename = new_filename.replace('{title}', title)
        new_filename = new_filename.replace('{author}', author)
        new_filename = new_filename.replace('{year}', year)
        new_filename = new_filename + file_ext
    else:
        # Default filename format
        new_filename = f"{title} - {author}{file_ext}"

    # Create the new directory path based on category (may include subdirectories)
    new_dir = os.path.join(output_dir, category)
    os.makedirs(new_dir, exist_ok=True)

    # Create the new full path for the file
    new_path = os.path.join(new_dir, new_filename)

    # Copy the file
    shutil.copy2(ebook_path, new_path)

    return new_path

# The process_batch function has already been replaced

def organize_ebooks(ebook_directory, categories, output_dir, additional_instructions="", batch_size=1):
    """Organize ebooks according to categories and instructions.
    
    Args:
        ebook_directory (str): Directory containing ebook files to organize
        categories (list): List of example categories
        output_dir (str): Directory where organized ebooks will be copied
        additional_instructions (str): Custom instructions for the LLM
        batch_size (int): Number of books to process in a single LLM request
                          Set to 1 for individual processing
    """
    """Organize ebooks according to categories and instructions."""

    # Determine if we should use default categories or custom ones from instructions
    use_default_categories = True
    if additional_instructions and ("organize them into directories named after" in additional_instructions or
                                  "custom categories" in additional_instructions):
        use_default_categories = False
        print("Using custom categorization from instructions file")

    # Get existing categories from output directory if it exists
    existing_categories = []
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        existing_categories = [d for d in os.listdir(output_dir)
                             if os.path.isdir(os.path.join(output_dir, d))]
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

    # Process books in batches if batch_size > 1, otherwise process individually
    if batch_size > 1 and len(ebook_files) > 1:
        print(f"Processing books in batches of up to {batch_size}")
        for i in range(0, len(ebook_files), batch_size):
            batch = ebook_files[i:i+batch_size]
            print(f"\nProcessing batch {i//batch_size + 1} ({len(batch)} books)")
            
            # Process the batch with retries if needed
            batch_results = process_batch(batch, categories, additional_instructions, 
                                         use_default_categories, existing_categories, max_retries=1)
            
            # Handle each result in the batch
            for ebook_dict in batch_results:
                # Handle category assignment
                category = ebook_dict.get("category", "Uncategorized")

                # Keep the original format but replace any problematic characters except slashes
                # We allow slashes for hierarchical categories like Technology/Python
                ebook_dict["category"] = category.replace(":", "-").replace("\\", "-")
                
                # Check for empty category - this would be the only case we override
                if not ebook_dict["category"] or ebook_dict["category"] == "":
                    ebook_dict["category"] = "Uncategorized"

                # Get the final category
                category = ebook_dict['category']

                # If this is a new category, add it to our existing categories list
                if category not in existing_categories:
                    existing_categories.append(category)
                    print(f"Added new category: {category}")
                    
                    # If it's a hierarchical category, also add the parent category
                    if '/' in category:
                        parent_category = category.split('/', 1)[0]
                        if parent_category and parent_category not in existing_categories:
                            existing_categories.append(parent_category)
                            print(f"Added parent category: {parent_category}")

                # Copy the ebook and store its new location
                ebook_dict['location'] = copy_ebook(ebook_dict['original_path'], ebook_dict, output_dir)

                print(f"Processed: {os.path.basename(ebook_dict['original_path'])} → {ebook_dict['category']}")
                organized_files.append(ebook_dict)
                
    else:
        # Original individual processing
        for ebook_path in ebook_files:
            print(f"Processing {ebook_path}...")

            ebook_dict = generate_ebook_dict(ebook_path, categories, additional_instructions, use_default_categories, existing_categories)

            # Handle category assignment
            category = ebook_dict.get("category", "Uncategorized")

            # Keep the original format but replace any problematic characters except slashes
            # We allow slashes for hierarchical categories like Technology/Python
            ebook_dict["category"] = category.replace(":", "-").replace("\\", "-")
            
            # Check for empty category - this would be the only case we override
            if not ebook_dict["category"] or ebook_dict["category"] == "":
                ebook_dict["category"] = "Uncategorized"

            # Get the final category
            category = ebook_dict['category']

            # If this is a new category, add it to our existing categories list
            if category not in existing_categories:
                existing_categories.append(category)
                print(f"Added new category: {category}")
                
                # If it's a hierarchical category, also add the parent category
                if '/' in category:
                    parent_category = category.split('/', 1)[0]
                    if parent_category and parent_category not in existing_categories:
                        existing_categories.append(parent_category)
                        print(f"Added parent category: {parent_category}")

            # Copy the ebook and store its new location
            ebook_dict['location'] = copy_ebook(ebook_path, ebook_dict, output_dir)

            print(f"Post-copy ebook_dict:\n{ebook_dict}")
            organized_files.append(ebook_dict)

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