import os
import requests
from bs4 import BeautifulSoup
import re
import zipfile
from urllib.parse import urljoin, unquote
from pathlib import Path

# Base directories
BASE_DIR = Path("product_documents")
ZIP_NAME = "ac_documents.zip"

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
            
            # Skip if file already exists
            if os.path.exists(filepath):
                print(f"Skipping existing file: {filepath}")
                continue
                
            print(f"Downloading {filename}...")
            download_file(pdf_url, filepath)
            
    except Exception as e:
        print(f"Error processing greecomfort.com: {e}")

def process_tosot_direct():
    """Process documents from tosotdirect.com"""
    base_url = "https://tosotdirect.com"
    url = f"{base_url}/pages/product-document"
    
    try:
        print(f"Fetching documents from {url}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all download links (they have class 'download-items')
        download_links = soup.find_all('a', class_='download-items', href=True)
        
        if not download_links:
            print("No download links found on the page. The page structure might have changed.")
            return
            
        print(f"Found {len(download_links)} potential document links")
        
        # Process each download link
        for link in download_links:
            pdf_url = link['href']
            if '.pdf' not in pdf_url.lower():
                continue
                
            # Some URLs might be relative, so join with base URL if needed
            if not pdf_url.startswith(('http://', 'https://')):
                pdf_url = urljoin(base_url, pdf_url)
            
            # Extract filename from URL and clean it up
            filename = unquote(pdf_url.split('/')[-1].split('?')[0])  # Remove query parameters
            
            # Determine document type from URL/filename
            doc_type = "other"
            filename_lower = filename.lower()
            if 'manual' in filename_lower or 'user' in filename_lower or 'guide' in filename_lower:
                doc_type = "user-manual"
            elif 'spec' in filename_lower or 'certif' in filename_lower or 'compliance' in filename_lower:
                doc_type = "technical-specs"
            elif 'catalog' in filename_lower or 'brochure' in filename_lower:
                doc_type = "marketing"
            
            # Create directory structure: brand/model/type/
            brand = "TOSOT"
            model = "General"
            
            # Try to extract model from filename (common patterns in Tosot filenames)
            model_match = re.search(r'(?:TST-|TOSOT[-_]?)([A-Z0-9-]+?)(?:-|_|$)', filename, re.IGNORECASE)
            if model_match:
                model = model_match.group(1).strip('-_').upper()
            
            # Clean up model name (remove version numbers or other suffixes)
            model = re.sub(r'[-_]?[vV]\d+', '', model)  # Remove version numbers like v1, v2, etc.
            model = re.sub(r'[-_]?[0-9]{6,}', '', model)  # Remove long number sequences (often dates)
            
            # Create directory path
            dir_path = BASE_DIR / brand / model / doc_type
            os.makedirs(dir_path, exist_ok=True)
            
            # Download file
            filepath = dir_path / filename
            
            # Skip if file already exists
            if os.path.exists(filepath):
                print(f"Skipping existing file: {filepath}")
                continue
                
            print(f"Downloading {filename}...")
            #if download_file(pdf_url, filepath):
            #    print(f"  -> Saved to: {filepath}")
            
    except Exception as e:
        print(f"Error processing tosotdirect.com: {e}")
        import traceback
        traceback.print_exc()
            
    except Exception as e:
        print(f"Error processing tosotdirect.com: {e}")

def create_zip():
    """Create a ZIP archive of the downloaded files with progress indication."""
    print(f"Creating {ZIP_NAME}...")
    
    # First, count total files to process
    total_files = 0
    for root, _, files in os.walk(BASE_DIR):
        total_files += len(files)
    
    if total_files == 0:
        print("No files found to archive.")
        return False
    
    processed_files = 0
    last_percent = -1
    
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(BASE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.join(BASE_DIR, '..'))
                zipf.write(file_path, arcname)
                
                # Update progress
                processed_files += 1
                percent_complete = int((processed_files / total_files) * 100)
                if percent_complete != last_percent:  # Only update when percentage changes
                    last_percent = percent_complete
                    print(f"\rProgress: {percent_complete}% ({processed_files}/{total_files} files)", end="")
    
    print(f"\nSuccessfully created {ZIP_NAME} ({os.path.getsize(ZIP_NAME) / (1024*1024):.2f} MB)")
    return True

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
