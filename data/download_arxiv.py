"""
    Performs query on "NVIDIA internal research"
    See below for current query (80-most recent NVIDIA-published AI/ML papers)
    Downloads PDF files from XML metadata (export.arxiv.org) to /arxiv_papers/
"""
import requests
import feedparser
import urllib.parse
import os
import time
import json 


def check_arxiv_for_doi(doi):
    """Checks arXiv API for a paper using its DOI and returns the PDF link if found."""
    if not doi or doi == 'no-doi':
        return None
        
    # The arXiv API supports searching by the DOI tag: 'doi:'
    ARXIV_API_URL = 'http://export.arxiv.org/api/query?'
    
    params = {
        'search_query': f'doi:{doi}',
        'max_results': 1,
    }
    query_url = ARXIV_API_URL + urllib.parse.urlencode(params)
    
    # Respect the rate limit before the lookup
    time.sleep(3) 
    try:
        response = requests.get(query_url, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        
        if feed.entries:
            entry = feed.entries[0]
            # Extract the direct PDF link (which will be an arxiv.org link)
            pdf_link = next((link['href'] for link in entry.links if link.get('type') == 'application/pdf'), None)
            if pdf_link:
                # Return the export server URL for safe download
                return pdf_link.replace('http://arxiv.org/', 'http://export.arxiv.org/')
                
    except requests.exceptions.RequestException as e:
        # Log the error but continue to the publisher link as a fallback
        print(f"   [DOI Check Failed] Error retrieving data for DOI {doi}: {e}")
        
    return None

# The validated OpenAlex ID for NVIDIA Corporation
# NVIDIA_INSTITUTION_ID = 'I1304085615' # UK CORP, has less citations than USA
NVIDIA_INSTITUTION_ID = 'I4210127875' # USA

# The high-precision, high-impact query parameters
QUERY_KEYWORDS = '("CUDA" OR "TensorRT" OR "DGX" OR "LLM")'
OPENALEX_API_URL = 'https://api.openalex.org/works'
MAX_RESULTS = 200
EMAIL_FOR_POLITE_POOL = 'notseng@ucsd.edu' 

# Output directory for downloaded PDFs
# OUTPUT_DIR = 'nvidia_top_100_pdfs'
OUTPUT_DIR = 'nvidia-most-cited'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# BUILD AND EXECUTE THE OPENALEX QUERY with filters, sorting, and field selection
params = {
    'search': QUERY_KEYWORDS,
    'filter': f'authorships.institutions.id:{NVIDIA_INSTITUTION_ID}',
    'sort': 'cited_by_count:desc',
    'per-page': MAX_RESULTS,
    'select': 'id,doi,title,cited_by_count,primary_location,authorships', # Fields to retrieve
    'mailto': EMAIL_FOR_POLITE_POOL
}

query_url = OPENALEX_API_URL + '?' + urllib.parse.urlencode(params)
print(f"Querying OpenAlex for top {MAX_RESULTS} affiliated papers...")

try:
    response = requests.get(query_url, timeout=60)
    response.raise_for_status() # Check for HTTP errors

    data = response.json()
    papers = data.get('results', [])
    total_found = data.get('meta', {}).get('count', 0)
    
    print(f"Successfully retrieved {len(papers)} of {total_found} total matching papers.")
    if not papers:
        print("No papers found matching the strict filters. Check the query and affiliation ID.")
        exit()

except requests.exceptions.RequestException as e:
    print(f"Error executing OpenAlex API query: {e}")
    exit()

# --- 3. DOWNLOAD PDFS AND HANDLE SOURCE ---

download_count = 0
for i, paper in enumerate(papers):
    
    title = paper.get('title', 'No Title').replace('\n', ' ').strip()
    doi_full_url = paper.get('doi')
    doi_id = doi_full_url.split('/')[-1] if doi_full_url else 'no-doi'
    cited_by = paper.get('cited_by_count', 0)
    
    # Filename remains the same:
    filename_snippet = "".join(c for c in title[:40] if c.isalnum() or c in (' ')).strip().replace(' ', '_')
    filename = os.path.join(OUTPUT_DIR, f"{doi_id}_CITED-{cited_by}_{filename_snippet}.pdf")
    
    print(filename)
    print("DOI: " + doi_id)
    print(f"\n[{i + 1}/{len(papers)}] Processing: {title} (Cited: {cited_by})")
    
    # --- A. STRATEGY: Check ArXiv First (PIRACY-FREE OPEN ACCESS) ---
    final_pdf_url = None
    if doi_full_url:
        final_pdf_url = check_arxiv_for_doi(doi_full_url)

    if final_pdf_url:
        print("-> ARXİV BYPASS SUCCESS: Using open-access arXiv PDF.")
        # Proceed to download using the trusted arXiv URL
    else:
        # --- B. STRATEGY: Fallback to OpenAlex/Publisher Link ---
        primary_location = paper.get('primary_location', {})
        if primary_location:
            final_pdf_url = primary_location.get('pdf_url') # Try direct PDF first
            if not final_pdf_url:
                final_pdf_url = primary_location.get('landing_page_url') # Fallback to landing page

        if not final_pdf_url:
            print("-> SKIPPING: No valid download link found.")
            continue
            
    # --- C. ATTEMPT DOWNLOAD ---
    try:
        # Use the determined final_pdf_url (either ArXiv or Publisher/Landing Page)
        pdf_response = requests.get(final_pdf_url, stream=True, timeout=60)
        pdf_response.raise_for_status()

        # Check content type (Application/pdf check is crucial here)
        content_type = pdf_response.headers.get('Content-Type', '').lower()
        
        if 'application/pdf' in content_type:
            with open(filename, 'wb') as f:
                for chunk in pdf_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            source_type = "arXiv" if "arxiv.org" in final_pdf_url else "Direct OA"
            print(f"-> SUCCESS ({source_type}): Saved as {filename}")
            download_count += 1
        else:
            # The URL led to a landing page, HTML, or paywall, not a direct PDF file.
            print(f"-> PAYWALL/LANDING PAGE: Download failed. URL: {final_pdf_url}")
            print(f"-> PAYWALL/LANDING PAGE: Download failed. DOI: {final_pdf_url}")

    except requests.exceptions.RequestException as e:
        print(f"-> NETWORK/TIMEOUT ERROR: Failed to access {final_pdf_url}. Error: {e}")

# ... (Part 4: Conclusion) ...
# --- 4. CONCLUSION ---
print("\n--- Process Complete ---")
print(f"Total papers processed: {len(papers)}")
print(f"Total PDFs successfully downloaded: {download_count}")
print("NOTE: Failed downloads = paywalls. Use institutional access to retrieve.")