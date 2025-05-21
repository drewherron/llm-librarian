# LLM Librarian

A command-line tool that uses AI to automatically organize your ebook collection. It supports PDF, EPUB, MOBI, and AZW3 files.

This is based on a school project I did a while ago. It works, but not quite well as I'd originally hoped... I may come back to it when I have more time.

## Features

- Extract metadata and content from multiple ebook formats
- Use AI to identify title, author, publication year, and categorize content
- Customize organization with instruction files
- Copy files to categorized directories with consistent naming
- Support for PDF, EPUB, MOBI, and AZW3 formats

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/drewherron/llm-librarian.git
   cd llm-librarian
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_api_key
   ```

## Usage

Basic usage:
```bash
python llm_librarian.py /path/to/ebooks /path/to/output
```

With custom organization instructions:
```bash
python llm_librarian.py /path/to/ebooks /path/to/output -i instructions.txt
```

## Custom Instructions

You can create text files with custom instructions for how to organize your ebooks. For example:

```
Only organize books about programming.
Organize them into directories named after the programming language.
Use the following format for filenames: {year} - {title} - {author}
```
