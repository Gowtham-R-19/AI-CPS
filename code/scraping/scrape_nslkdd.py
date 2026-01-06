"""
NSL-KDD Dataset Web Scraping Script
Course: M. Grum: Advanced AI-based Application Systems
University of Potsdam

This script scrapes the NSL-KDD dataset from the official UNB website.
"""

import requests
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path


def scrape_nslkdd_dataset():
    """
    Scrape NSL-KDD dataset from official UNB website.
    
    Target URL: https://www.unb.ca/cic/datasets/nsl.html
    
    Expected files:
    - KDDTrain+.txt (Training data)
    - KDDTest+.txt (Testing data)
    - KDDTrain+_20Percent.txt (Quick testing subset)
    - KDDTest-21.txt (Harder test set)
    """
    
    # Configuration
    base_url = "https://www.unb.ca/cic/datasets/nsl.html"
    output_dir = Path("../../data/raw")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set user agent to identify as academic scraper
    headers = {
        'User-Agent': 'Mozilla/5.0 (Academic Research) University of Potsdam/1.0'
    }
    
    print("🌐 Starting NSL-KDD dataset scraping...")
    print(f"📍 Target URL: {base_url}")
    print(f"📁 Output directory: {output_dir.absolute()}")
    
    try:
        # Step 1: Fetch the webpage
        print("\n⏳ Fetching webpage...")
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        print("✅ Webpage fetched successfully")
        
        # Step 2: Parse HTML
        print("\n⏳ Parsing HTML...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Step 3: Find all download links
        print("\n⏳ Searching for dataset download links...")
        
        # Look for links containing 'KDD' in href
        download_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'KDD' in href or 'nsl-kdd' in href.lower():
                # Build full URL if relative path
                if not href.startswith('http'):
                    full_url = f"https://www.unb.ca{href}" if href.startswith('/') else f"https://www.unb.ca/cic/datasets/{href}"
                else:
                    full_url = href
                    
                download_links.append({
                    'url': full_url,
                    'filename': os.path.basename(href)
                })
        
        print(f"✅ Found {len(download_links)} potential download links")
        
        # Step 4: Download files
        if not download_links:
            print("⚠️  No download links found. You may need to:")
            print("   1. Check if the website structure has changed")
            print("   2. Use manual download from: https://www.unb.ca/cic/datasets/nsl.html")
            print("   3. Try Kaggle mirror: https://www.kaggle.com/datasets/hassan06/nslkdd")
            return False
        
        for link_info in download_links:
            url = link_info['url']
            filename = link_info['filename']
            filepath = output_dir / filename
            
            print(f"\n⏳ Downloading: {filename}")
            print(f"   URL: {url}")
            
            try:
                # Be polite: wait 1-2 seconds between requests
                time.sleep(2)
                
                file_response = requests.get(url, headers=headers, stream=True)
                file_response.raise_for_status()
                
                # Save file
                with open(filepath, 'wb') as f:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = filepath.stat().st_size / (1024 * 1024)  # Size in MB
                print(f"✅ Downloaded: {filename} ({file_size:.2f} MB)")
                
            except Exception as e:
                print(f"❌ Error downloading {filename}: {str(e)}")
        
        print("\n✅ Scraping completed!")
        print(f"📁 Check files in: {output_dir.absolute()}")
        return True
        
    except requests.RequestException as e:
        print(f"❌ Error fetching webpage: {str(e)}")
        print("\n💡 Manual Download Instructions:")
        print("   1. Visit: https://www.unb.ca/cic/datasets/nsl.html")
        print("   2. Download these files manually:")
        print("      - KDDTrain+.txt")
        print("      - KDDTest+.txt")
        print("   3. Place them in: data/raw/")
        return False


def verify_downloaded_files():
    """
    Verify that required dataset files exist.
    """
    required_files = [
        'KDDTrain+.txt',
        'KDDTest+.txt'
    ]
    
    output_dir = Path("../../data/raw")
    
    print("\n🔍 Verifying downloaded files...")
    all_present = True
    
    for filename in required_files:
        filepath = output_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size / (1024 * 1024)
            print(f"✅ {filename} - {size:.2f} MB")
        else:
            print(f"❌ {filename} - NOT FOUND")
            all_present = False
    
    return all_present


if __name__ == "__main__":
    print("="*60)
    print("NSL-KDD DATASET WEB SCRAPING")
    print("Course: M. Grum: Advanced AI-based Application Systems")
    print("University of Potsdam")
    print("="*60)
    
    # Run scraping
    success = scrape_nslkdd_dataset()
    
    # Verify files
    if success:
        verify_downloaded_files()
    
    print("\n" + "="*60)
    print("NEXT STEP: Run preprocessing script")
    print("Command: python code/preprocessing/preprocess_data.py")
    print("="*60)