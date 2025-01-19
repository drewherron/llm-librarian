# Ebook Organizer

A command-line tool that helps organize ebook collections. It supports PDF, EPUB, MOBI, and AZW3 files.

## Features

- Extract metadata and content from multiple ebook formats
- Categorize books based on content analysis
- Customize organization with instruction files
- Copy files to categorized directories with consistent naming
- Support for PDF, EPUB, MOBI, and AZW3 formats

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ebook-organizer.git
   cd ebook-organizer
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Basic usage:
```bash
python ebook_organizer.py /path/to/ebooks /path/to/output
```

With custom organization instructions:
```bash
python ebook_organizer.py /path/to/ebooks /path/to/output -i instructions.txt
```

## Custom Instructions

You can create text files with custom instructions for how to organize your ebooks. For example:

```
Only organize books about programming.
Organize them into directories named after the programming language.
Use the following format for filenames: {title} - {author} - {year}
```

See `instructions_example.txt` for a more detailed example.

## Notes

- The program copies files rather than moving them, so your original files remain intact
- MOBI and AZW3 support is basic due to limited metadata extraction capabilities