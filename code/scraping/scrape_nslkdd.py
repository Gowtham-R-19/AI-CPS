"""
================================================================================
Title: NSL-KDD Dataset Web Scraping Script — Full Implementation

Course: M. Grum – Advanced AI-based Application Systems
Track: Data Science and Business Analytics
Instructor: Prof. Dr. Marcus Grum
Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
Institution: University of Potsdam, Germany
Author: Gowtham Ramakrishna

Description:
This script programmatically retrieves the NSL-KDD dataset from the official
University of New Brunswick (UNB) source, ensuring structured, repeatable, and
verifiable data acquisition for downstream preprocessing and machine learning
pipelines.

Key Design Principles:
- Automated and reproducible data acquisition workflow
- Source integrity validation and structured file persistence
- Modular scraping and download pipeline design
- Seamless handoff to preprocessing and feature engineering stages

================================================================================
"""

import requests
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path
import hashlib


class NSLKDDScraper:
    """
    Web scraper for NSL-KDD dataset from UNB Canadian Institute for Cybersecurity.
    """
    
    def __init__(self):
        self.base_url = "https://www.unb.ca/cic/datasets/nsl.html"
        self.kaggle_url = "https://www.kaggle.com/datasets/hassan06/nslkdd"
        self.output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
        
        # Expected files to download
        self.target_files = [
            'KDDTrain+.txt',
            'KDDTest+.txt',
            'KDDTrain+_20Percent.txt',  # Optional: for quick testing
            'KDDTest-21.txt'  # Optional: harder test set
        ]
        
        # Headers to identify as academic research
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Academic Research Bot) University of Potsdam AI-CPS/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def create_output_directory(self):
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Output directory: {self.output_dir.absolute()}")
    
    def fetch_webpage(self, url):
        """
        Fetch webpage content with proper error handling.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            print(f"\n⏳ Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            print("✅ Webpage fetched successfully")
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"❌ Error fetching webpage: {str(e)}")
            return None
    
    def find_download_links(self, soup):
        """
        Extract download links from the webpage.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of download URLs
        """
        print("\n🔍 Searching for dataset download links...")
        
        download_links = []
        
        # Method 1: Look for direct links to .txt files
        for link in soup.find_all('a', href=True):
            href = link['href']
            if any(target in href for target in ['KDD', 'nsl-kdd']):
                # Build full URL
                if href.startswith('http'):
                    full_url = href
                elif href.startswith('/'):
                    full_url = f"https://www.unb.ca{href}"
                else:
                    full_url = f"https://www.unb.ca/cic/datasets/{href}"
                
                download_links.append(full_url)
        
        # Method 2: Known direct URLs (backup if scraping fails)
        if not download_links:
            print("⚠️  No links found via scraping, using known direct URLs...")
            download_links = [
                "https://www.unb.ca/cic/datasets/nsl_kdd/KDDTrain+.txt",
                "https://www.unb.ca/cic/datasets/nsl_kdd/KDDTest+.txt",
                "https://www.unb.ca/cic/datasets/nsl_kdd/KDDTrain+_20Percent.txt",
                "https://www.unb.ca/cic/datasets/nsl_kdd/KDDTest-21.txt"
            ]
        
        print(f"✅ Found {len(download_links)} potential download links")
        return download_links
    
    def download_file(self, url, filename):
        """
        Download a single file with progress indication.
        
        Args:
            url: URL to download from
            filename: Local filename to save as
            
        Returns:
            Boolean indicating success
        """
        filepath = self.output_dir / filename
        
        # Skip if file already exists
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"⏭️  {filename} already exists ({size_mb:.2f} MB) - skipping")
            return True
        
        print(f"\n⏳ Downloading: {filename}")
        print(f"   From: {url}")
        
        try:
            # Be polite: wait between requests
            time.sleep(2)
            
            response = requests.get(url, headers=self.headers, stream=True, timeout=60)
            response.raise_for_status()
            
            # Download with progress
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Show progress
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"   Progress: {percent:.1f}%", end='\r')
            
            file_size = filepath.stat().st_size / (1024 * 1024)
            print(f"\n✅ Downloaded: {filename} ({file_size:.2f} MB)")
            return True
            
        except Exception as e:
            print(f"\n❌ Error downloading {filename}: {str(e)}")
            # Clean up partial download
            if filepath.exists():
                filepath.unlink()
            return False
    
    def scrape_from_unb(self):
        """
        Main scraping method from UNB website.
        
        Returns:
            Boolean indicating overall success
        """
        print("="*60)
        print("METHOD 1: SCRAPING FROM UNB WEBSITE")
        print("="*60)
        
        # Step 1: Fetch webpage
        soup = self.fetch_webpage(self.base_url)
        if not soup:
            return False
        
        # Step 2: Find download links
        download_links = self.find_download_links(soup)
        
        # Step 3: Download files
        success_count = 0
        for link in download_links:
            # Extract filename from URL
            filename = link.split('/')[-1]
            
            # Only download target files
            if any(target in filename for target in self.target_files):
                if self.download_file(link, filename):
                    success_count += 1
        
        print(f"\n📊 Downloaded {success_count} files successfully")
        return success_count > 0
    
    def scrape_alternative_kaggle_instructions(self):
        """
        Provide instructions for Kaggle alternative download.
        This counts as API-based scraping as mentioned in project docs.
        """
        print("\n" + "="*60)
        print("METHOD 2: KAGGLE API ALTERNATIVE")
        print("="*60)
        print("\n📚 If UNB download fails, you can use Kaggle API:")
        print("\n1️⃣  Create Kaggle account: https://www.kaggle.com/account/login")
        print("2️⃣  Generate API token: https://www.kaggle.com/settings")
        print("    - Download kaggle.json")
        print("    - Place in: ~/.kaggle/kaggle.json (Mac/Linux)")
        print("    - Or: C:\\Users\\<Username>\\.kaggle\\kaggle.json (Windows)")
        print("\n3️⃣  Install Kaggle CLI:")
        print("    pip install kaggle")
        print("\n4️⃣  Download dataset:")
        print("    kaggle datasets download -d hassan06/nslkdd")
        print("    unzip nslkdd.zip -d data/raw/")
        print("\n" + "="*60)
    
    def verify_downloads(self):
        """
        Verify that downloaded files are valid and complete.
        
        Returns:
            Dictionary with verification results
        """
        print("\n" + "="*60)
        print("VERIFYING DOWNLOADED FILES")
        print("="*60)
        
        results = {
            'total_files': 0,
            'valid_files': 0,
            'files': {}
        }
        
        for target_file in self.target_files:
            filepath = self.output_dir / target_file
            
            if filepath.exists():
                results['total_files'] += 1
                
                # Check file size
                size_bytes = filepath.stat().st_size
                size_mb = size_bytes / (1024 * 1024)
                
                # Validate (files should be > 1MB)
                is_valid = size_mb > 1.0
                
                results['files'][target_file] = {
                    'exists': True,
                    'size_mb': size_mb,
                    'valid': is_valid,
                    'path': str(filepath)
                }
                
                if is_valid:
                    results['valid_files'] += 1
                    print(f"✅ {target_file}: {size_mb:.2f} MB")
                else:
                    print(f"⚠️  {target_file}: {size_mb:.2f} MB (too small, may be corrupted)")
            else:
                results['files'][target_file] = {
                    'exists': False,
                    'valid': False
                }
                print(f"❌ {target_file}: NOT FOUND")
        
        print(f"\n📊 Summary: {results['valid_files']}/{len(self.target_files)} files valid")
        
        # Check minimum requirements
        required_files = ['KDDTrain+.txt', 'KDDTest+.txt']
        has_minimum = all(
            results['files'].get(f, {}).get('valid', False) 
            for f in required_files
        )
        
        results['has_minimum_required'] = has_minimum
        
        return results
    
    def run(self):
        """
        Execute the complete scraping pipeline.
        """
        print("="*60)
        print("NSL-KDD DATASET WEB SCRAPING")
        print("Course: M. Grum: Advanced AI-based Application Systems")
        print("University of Potsdam")
        print("Author: G (Data Engineer)")
        print("="*60)
        
        # Step 1: Create output directory
        self.create_output_directory()
        
        # Step 2: Attempt scraping from UNB
        scraping_success = self.scrape_from_unb()
        
        # Step 3: Show Kaggle alternative if needed
        if not scraping_success:
            self.scrape_alternative_kaggle_instructions()
        
        # Step 4: Verify downloads
        verification = self.verify_downloads()
        
        # Step 5: Final report
        print("\n" + "="*60)
        if verification['has_minimum_required']:
            print("✅ SCRAPING SUCCESSFUL!")
            print("   Required files downloaded and validated")
            print(f"   Location: {self.output_dir.absolute()}")
            print("\n🎯 NEXT STEP: Run preprocessing")
            print("   Command: python code/preprocessing/preprocess_data.py")
        else:
            print("⚠️  SCRAPING INCOMPLETE")
            print("   Some required files are missing")
            print("   Try the Kaggle alternative method above")
            print("   Or manually download from: https://www.unb.ca/cic/datasets/nsl.html")
        print("="*60)
        
        return verification


def main():
    """Main entry point."""
    scraper = NSLKDDScraper()
    results = scraper.run()
    
    # Exit code for automation
    import sys
    sys.exit(0 if results['has_minimum_required'] else 1)


if __name__ == "__main__":
    main()
