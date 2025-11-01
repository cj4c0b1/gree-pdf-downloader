# PDF Downloader for GREE and TOSOT Documentation

This script downloads and organizes PDF documentation from GREE and TOSOT product websites into a structured folder hierarchy.

## Features

- Downloads PDFs from specified product documentation pages
- Organizes files in a clean directory structure: `brand/model/type/filename.pdf`
- Creates a ZIP archive of all downloaded documents
- Preserves original filenames

## Requirements

- Python 3.7+
- Required packages: See `requirements.txt`

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script:
```bash
python download_pdfs.py
```

The script will:
1. Create a `gree_documents` directory
2. Download PDFs from the specified websites
3. Organize them in the required folder structure
4. Create a `gree_documents.zip` archive

## Project Structure

```
.
├── download_pdfs.py    # Main script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## License

This project is for personal/educational use only. Please respect the copyright of the downloaded documents.
