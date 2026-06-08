import fitz  # This is PyMuPDF

def extract_raw_pdf(pdf_path):
    print("Opening PDF...")
    doc = fitz.open(pdf_path)
    full_text = ""
    
    # Loop through every single page of the PDF sequentially
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Extract text while trying to maintain layout blocks
        full_text += page.get_text("text") + "\n--- PAGE BREAK ---\n"
        
    return full_text

# Run the extraction
raw_data = extract_raw_pdf("contract.pdf")

import re

def clean_headers_footers(text):
    # Rule 1: Match things like "Page 4 of 20", "Page 4", or "4 of 20" at the end of lines
    text = re.sub(r'(?i)page\s+\d+(\s+of\s+\d+)?', '', text)
    
    # Rule 2: Match dates like "Dated: March 12, 2023" or "06/07/2026" stamping the pages
    text = re.sub(r'\d{2}/\d{2}/\d{4}|\w+\s+\d+,\s+\d{4}', '', text)
    
    # Rule 3: Strip out the page break placeholders we added in Step 2
    text = re.sub(r'--- PAGE BREAK ---', '', text)
    
    return text

def normalize_whitespace(text):
    # Rule 1: Fix broken words separated by a hyphen and a newline (e.g., "in- /n demnify")
    text = re.sub(r'-\s*\n\s*', '', text)
    
    # Rule 2: Turn multiple horizontal spaces or tabs into a single standard space
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Rule 3: Legal chunks need crisp paragraphs. 
    # If there are 3 or more consecutive newlines, collapse them into a clean double newline (\n\n)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

if __name__ == "__main__":
    # 1. Read
    raw_extracted = extract_raw_pdf("contract.pdf")
    
    # 2. Scrub headers
    no_headers = clean_headers_footers(raw_extracted)
    
    # 3. Fix spacing
    final_clean_text = normalize_whitespace(no_headers)
    
    # Save the results to a text file so he can inspect his work
    with open("cleaned_contract.txt", "w", encoding="utf-8") as f:
        f.write(final_clean_text)
        
    print("Success! Open 'cleaned_contract.txt' to view your perfect, normalized legal text.")

    