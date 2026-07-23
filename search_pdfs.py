import os
import fitz  # PyMuPDF
import re

pdf_dir = "Literature"
search_terms = {
    "fig2_1": re.compile(r"System overview of a typical unmanned ground vehicle", re.IGNORECASE),
    "fig2_2": re.compile(r"Architecture of the proposed autonomous navigation approach", re.IGNORECASE),
    "fig2_3": re.compile(r"Real-world 3D environment modeling results", re.IGNORECASE),
    "fig2_4": re.compile(r"Roadford Lake", re.IGNORECASE)
}

results = {k: [] for k in search_terms.keys()}

for filename in os.listdir(pdf_dir):
    if not filename.endswith(".pdf"):
        continue
    filepath = os.path.join(pdf_dir, filename)
    try:
        doc = fitz.open(filepath)
        for page_num in range(len(doc)):
            text = doc[page_num].get_text("text").replace('\n', ' ')
            for key, pattern in search_terms.items():
                if pattern.search(text):
                    results[key].append(filename)
                    break 
        doc.close()
    except Exception as e:
        print(f"Error reading {filename}: {e}")

for key, files in results.items():
    print(f"Matches for {key}:")
    for f in set(files):
        print(f"  - {f}")
