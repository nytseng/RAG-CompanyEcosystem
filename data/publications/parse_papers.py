"""
    Parses the folder "nvidia-most-cited" papers into plain text
    Saved in 'rag_papers_text'

"""
import nltk
import time
import requests
# ... other imports ...

# --- NLTK Resource Downloads ---
REQUIRED_NLTK_RESOURCES = [
    'punkt', 
    'averaged_perceptron_tagger'
]
for resource in REQUIRED_NLTK_RESOURCES:
    try:
        # Check if the resource is already installed
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        print(f"Downloading required NLTK resource '{resource}'...")
        # If not found, download it. The download function handles the core logic.
        nltk.download(resource)

from unstructured.partition.pdf import partition_pdf
import os
from pathlib import Path


INPUT_DIR = 'nvidia-most-cited'
# INPUT_DIR = 'selected_papers'
OUTPUT_DIR = 'rag_papers_text'
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# --- Processing Function ---
def extract_and_save_structured_text(pdf_path):
    """
    Extracts structured elements (text, titles, tables, etc.) from a PDF 
    and saves the content as a single Markdown file.
    """
    try:
        # Use partition to process the file and extract elements
        elements = partition_pdf(filename=pdf_path, languages=["eng"])
        
        # We can reconstruct the text in Markdown format, preserving hierarchy
        # The elements list automatically extracts and tags text, titles, lists, and tables
        markdown_content = "\n\n".join([
            str(e) for e in elements
        ])
        
        # Define output filename
        output_filename = Path(pdf_path).stem + ".md"
        output_path = Path(OUTPUT_DIR) / output_filename
        
        # Save the content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Success: Processed '{pdf_path.name}' -> '{output_filename}'")
        return True

    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")
        return False

# --- Main Execution ---
print(f"Starting extraction of PDFs from: {INPUT_DIR}")
pdf_files = list(Path(INPUT_DIR).glob('*.pdf'))
processed_count = 0

for pdf_path in pdf_files:
    if extract_and_save_structured_text(pdf_path):
        processed_count += 1
        
print(f"\n--- Extraction Summary ---")
print(f"Total PDFs found: {len(pdf_files)}")
print(f"Successfully converted to Markdown: {processed_count}")