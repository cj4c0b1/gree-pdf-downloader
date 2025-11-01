import os
import requests
from bs4 import BeautifulSoup
import re
import zipfile
from urllib.parse import urljoin, unquote
from pathlib import Path

# Base directories
BASE_DIR = Path("gree_documents")
ZIP_NAME = "gree_documents.zip"

# Create base directory if it doesn't exist
os.makedirs(BASE_DIR, exist_ok=True)

def sanitize_filename(filename):
    """Remove invalid characters from filenames."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def download_file(url, filepath):
    """Download a file from URL to the specified path."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def process_gree_comfort():
    """Process documents from greecomfort.com"""
    base_url = "https://www.greecomfort.com"
    url = f"{base_url}/system-documentation/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all PDF links
        pdf_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.lower().endswith('.pdf'):
                full_url = urljoin(base_url, href)
                pdf_links.append(full_url)
        
        # Download and organize PDFs
        for pdf_url in pdf_links:
            # Extract filename from URL
            filename = unquote(pdf_url.split('/')[-1])
            
            # Determine document type from URL
            doc_type = "other"
            if 'catalog' in pdf_url.lower():
                doc_type = "catalog"
            elif 'brochure' in pdf_url.lower() or 'literature' in pdf_url.lower():
                doc_type = "marketing"
            elif 'manual' in pdf_url.lower() or 'guide' in pdf_url.lower():
                doc_type = "user-manual"
            elif 'spec' in pdf_url.lower():
                doc_type = "technical-specs"
            
            # Create directory structure: brand/model/type/
            brand = "GREE"
            model = "General"  # Default model since we can't always determine from URL
            
            # Try to extract model from filename
            model_match = re.search(r'(?i)(flexx|xpac|mtac|multi\s*r32|single-?zone|multi-?zone)', filename)
            if model_match:
                model = model_match.group(1).replace(' ', '-').lower()
            
            # Create directory path
            dir_path = BASE_DIR / brand / model / doc_type
            os.makedirs(dir_path, exist_ok=True)
            
            # Download file
            filepath = dir_path / filename
            print(f"Downloading {pdf_url} to {filepath}")
            download_file(pdf_url, filepath)
            
    except Exception as e:
        print(f"Error processing greecomfort.com: {e}")

def process_tosot_direct():
    """Process documents from tosotdirect.com"""
    base_url = "https://tosotdirect.com"
    url = f"{base_url}/pages/product-document"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all PDF links - this might need adjustment based on actual page structure
        pdf_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.lower().endswith('.pdf'):
                full_url = urljoin(base_url, href)
                pdf_links.append(full_url)
        
        # Download and organize PDFs
        for pdf_url in pdf_links:
            # Extract filename from URL
            filename = unquote(pdf_url.split('/')[-1])
            
            # Determine document type from URL/filename
            doc_type = "other"
            if 'manual' in filename.lower() or 'guide' in filename.lower():
                doc_type = "user-manual"
            elif 'spec' in filename.lower():
                doc_type = "technical-specs"
            elif 'catalog' in filename.lower():
                doc_type = "catalog"
            
            # Create directory structure: brand/model/type/
            brand = "TOSOT"
            model = "General"
            
            # Try to extract model from filename
            model_match = re.search(r'(?i)([A-Z0-9-]+-?[A-Z0-9]*)', filename)
            if model_match:
                model = model_match.group(1)
            
            # Create directory path
            dir_path = BASE_DIR / brand / model / doc_type
            os.makedirs(dir_path, exist_ok=True)
            
            # Download file
            filepath = dir_path / filename
            print(f"Downloading {pdf_url} to {filepath}")
            download_file(pdf_url, filepath)
            
    except Exception as e:
        print(f"Error processing tosotdirect.com: {e}")

def create_zip():
    """Create a ZIP archive of the downloaded files."""
    print(f"Creating {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(BASE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.join(BASE_DIR, '..'))
                zipf.write(file_path, arcname)
    print(f"Created {ZIP_NAME}")

def main():
    print("Starting PDF download and organization...")
    
    # Process both websites
    process_gree_comfort()
    process_tosot_direct()
    
    # Create ZIP archive
    create_zip()
    
    print("\nProcess completed!")
    print(f"1. All PDFs have been downloaded and organized in the '{BASE_DIR}' directory.")
    print(f"2. A ZIP archive '{ZIP_NAME}' has been created with all the organized files.")
    print("\nTo use this script again, simply run: python download_pdfs.py")

if __name__ == "__main__":
    main()
