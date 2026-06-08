import re
import json

def structural_chunker(text_filepath):
    # 1. Read the clean text file generated from Step 1
    with open(text_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Define regex patterns for typical legal headings
    # These look for lines starting exactly with "ARTICLE I", "Article 2", "SECTION 1.01", or "Section 4.1"
# 2. Match section numbers followed by ALL CAPS titles anywhere in the text.
    # It catches "1. SERVICES", "2. COMPENSATION", etc., even mid-paragraph!
    combined_pattern = r'(\d+\.\s+[A-Z\s]{4,}(?=\s))'
    
    # Find all the matching section headers
    boundaries = list(re.finditer(combined_pattern, content))
    
    chunks = []
    start_pos = 0
    current_heading = "PREAMBLE / GENERAL"
    
    print(f"Found {len(boundaries)} structural inline headers in the contract.")
    chunks = []
    start_pos = 0
    current_heading = "PREAMBLE / GENERAL"
    
    print(f"Found {len(boundaries)} structural headers in the contract.")

# 4. Loop through boundaries and slice
    for match in boundaries:
        end_pos = match.start()
        chunk_body = content[start_pos:end_pos].strip()
        
        if chunk_body:
            chunks.append({
                "parent_context": current_heading,
                "text": chunk_body
            })
            
        # Update trackers for the next segment
        start_pos = end_pos
        current_heading = match.group(0).strip()
        
    # 5. Capture the last chunk
    last_chunk_body = content[start_pos:].strip()
    if last_chunk_body:
        chunks.append({
            "parent_context": current_heading,
            "text": last_chunk_body
        })
        
    return chunks

if __name__ == "__main__":
    # Execute the chunking function
    processed_chunks = structural_chunker("cleaned_contract.txt")
    
    # Save the structured array as a JSON file so it can be fed into a Vector DB later
    with open("structured_chunks.json", "w", encoding="utf-8") as f:
        json.dump(processed_chunks, f, indent=4, ensure_ascii=False)
        
    print("Success! Created 'structured_chunks.json' with perfect legal boundaries.")