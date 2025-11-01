# AC Product Documentation Downloader

This script downloads and organizes PDF documentation from various air conditioning product manufacturers (currently GREE and TOSOT) into a structured folder hierarchy.

## Features

- Downloads PDFs from product documentation pages
- Organizes files in a clean, consistent directory structure (see below)
- Creates a ZIP archive (`ac_documents.zip`) of all downloaded documents
- Preserves original filenames while organizing them logically
- Skips already downloaded files to save bandwidth

## Directory Structure

```
product_documents/
├── GREE/
│   ├── Model1/
│   │   ├── user-manual/
│   │   ├── technical-specs/
│   │   └── marketing/
│   └── Model2/
│       └── ...
└── TOSOT/
    ├── ModelA/
    │   ├── user-manual/
    │   └── technical-specs/
    └── ModelB/
        └── ...
```

Document types are automatically categorized into:
- `user-manual/`: User guides and instruction manuals
- `technical-specs/`: Technical specifications, certificates, and compliance documents
- `marketing/`: Catalogs, brochures, and marketing materials
- `other/`: Any documents that don't fit the above categories

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

## Donations

If you find this project useful, consider supporting its development:

- **EVM Wallet**: `0x7B267EcEc11a07CA2a782E4b8a51558a70449e7c`

Your support is greatly appreciated and helps maintain and improve this tool.
