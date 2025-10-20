import requests
from bs4 import BeautifulSoup
from time import sleep
import os
import re

# The base URL for the NVIDIA Newsroom "Latest News" archive
BASE_URL = "https://nvidianews.nvidia.com/news/latest"

# Maximum number of archive pages to scrape (Adjust this number as needed)
MAX_PAGES = 3

# Directory where the text files will be saved
OUTPUT_DIR = "nvidia_articles"

# --- Setup and Utility Functions ---

def setup_directory():
    """Creates the output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory '{OUTPUT_DIR}' ensured.")

def clean_filename(title):
    """Cleans the article title to create a safe filename."""
    # Replace non-alphanumeric characters (except space, hyphen, underscore) with an underscore
    title = re.sub(r'[^\w\s-]', '', title).strip()
    # Replace spaces/hyphens with a single underscore
    title = re.sub(r'[-\s]+', '_', title)
    # Truncate to a reasonable length
    return title[:100] + ".txt"

def get_page_content(url):
    """Fetches the content of a single URL."""
    try:
        # Use a generic User-Agent for better compatibility
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_article_content(article_url):
    """Scrapes the main text content and title from an individual article page."""
    html = get_page_content(article_url)
    if not html:
        return None, None

    soup = BeautifulSoup(html, 'html.parser')
    
    # Try to get the title from the main H1 tag
    title_tag = soup.find('h1', class_='header-innerpage-title') or soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

    # --- REVISED CONTENT AREA SELECTOR ---
    # Based on the typical structure of NVIDIA's news/blog articles.
    # Looking for a main content container, often a div with a class like 'article-body'
    content_area = soup.find('div', class_='article-body') 
    
    if not content_area:
        # Fallback for pages without a clear 'article-body' class (e.g., blog posts)
        # We'll try to find the main <article> or a well-known post container
        content_area = soup.find('article', class_='index-item-detail') or soup.find('div', id='content')


    if not content_area:
        print(f"Warning: Could not find main content for {article_url}")
        return title, None

    # Extract all text from the content area, cleaning up whitespace
    text_content = content_area.get_text(separator='\n', strip=True)
    
    # Prepend the URL and Title to the document content for completeness
    full_content = f"Title: {title}\nSource: {article_url}\n\n---\n\n{text_content}"

    return title, full_content

def save_article_to_file(filename, content):
    """Saves the text content to a file in the output directory."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   💾 Saved to: {filepath}")
        return True
    except IOError as e:
        print(f"Error saving file {filepath}: {e}")
        return False

# --- Main Scraper Logic ---

def scrape_and_save_newsroom():
    """Iterates through the news archive pages, scrapes articles, and saves them."""
    setup_directory()
    articles_saved_count = 0
    
    print(f"Starting scrape from {BASE_URL}...")
    
    for page_num in range(1, MAX_PAGES + 1):
        archive_url = f"{BASE_URL}?page={page_num}" if page_num > 1 else BASE_URL
        print(f"\n--- Scraping Archive Page {page_num} ({archive_url}) ---")
        
        archive_html = get_page_content(archive_url)
        if not archive_html:
            break

        archive_soup = BeautifulSoup(archive_html, 'html.parser')
        
        # --- REVISED ARTICLE LINK SELECTOR ---
        # Targets <a> tags directly inside the h3.index-item-text-title class, 
        # which is the structure shown in your HTML snippet.
        article_link_tags = archive_soup.select('h3.index-item-text-title > a')
        
        if not article_link_tags:
            print("No more article links found or end of archive reached.")
            break

        print(f"Found {len(article_link_tags)} article links.")

        for link_tag in article_link_tags:
            full_article_url = link_tag['href']

            # Ensure the link is absolute, or prepend the base URL if it's relative
            if full_article_url.startswith('/'):
                full_article_url = f"https://nvidianews.nvidia.com{full_article_url}"
            
            # Skip links that point to external blogs unless you want to scrape them, 
            # which may require different selectors. We'll scrape everything for now.
            print(f"-> Processing: {full_article_url}")

            title, content = extract_article_content(full_article_url)

            if content:
                filename = clean_filename(title)
                if save_article_to_file(filename, content):
                    articles_saved_count += 1
            
            # Be polite and wait between requests
            sleep(0.5) 
            
    print("\n--- Scraping Complete ---")
    print(f"Total articles saved: {articles_saved_count} files in '{OUTPUT_DIR}/'")
    
    print("\nThese text files are now ready to be loaded into your vectorstore using a Directory Loader.")

# Run the scraper
scrape_and_save_newsroom()