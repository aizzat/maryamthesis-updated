import os
import re
import glob
import difflib

def read_bib(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = {}
    # match @type{key, ...}
    for match in re.finditer(r'@(\w+)\s*\{\s*([^,]+),', content):
        start = match.start()
        entry_type = match.group(1)
        key = match.group(2).strip()
        
        # Find the end of this entry by counting braces
        brace_count = 0
        in_entry = False
        end = -1
        for i in range(match.end() - 1, len(content)):
            if content[i] == '{':
                brace_count += 1
                in_entry = True
            elif content[i] == '}':
                brace_count -= 1
            
            if in_entry and brace_count == 0:
                end = i + 1
                break
        
        if end != -1:
            raw_text = content[start:end]
            entries[key] = {
                'type': entry_type,
                'raw': raw_text
            }
    return entries, content

def write_bib(filepath, entries, keep_keys):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("%% rujukan.bib - Cleaned and Verified\n")
        f.write("%% Automatically generated to match exactly cited keys\n\n")
        for key in sorted(keep_keys):
            if key in entries:
                f.write(entries[key]['raw'] + "\n\n")

def get_tex_files():
    tex_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.tex'):
                tex_files.append(os.path.join(root, f))
    return tex_files

def extract_tex_keys(tex_files):
    tex_keys = {}
    pat = re.compile(r'\\cite[p|t]?\{([^}]+)\}')
    for tex in tex_files:
        with open(tex, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for m in pat.finditer(content):
            keys = [k.strip() for k in m.group(1).split(',')]
            for k in keys:
                if k not in tex_keys:
                    tex_keys[k] = []
                tex_keys[k].append(tex)
    return tex_keys

def get_pdfs():
    pdfs = []
    pdf_dir = 'Literature'
    if os.path.exists(pdf_dir):
        for f in os.listdir(pdf_dir):
            if f.lower().endswith('.pdf'):
                pdfs.append(f[:-4]) # remove .pdf
    return pdfs

def main():
    bib_entries, raw_bib = read_bib('rujukan.bib')
    tex_files = get_tex_files()
    tex_keys_map = extract_tex_keys(tex_files)
    
    tex_keys = set(tex_keys_map.keys())
    bib_keys = set(bib_entries.keys())
    
    orphans = bib_keys - tex_keys
    missing = tex_keys - bib_keys
    
    pdfs = get_pdfs()
    
    report = []
    report.append("=== Citation Verification Report ===")
    report.append(f"Total keys in .tex files: {len(tex_keys)}")
    report.append(f"Total entries in rujukan.bib: {len(bib_keys)}")
    
    report.append(f"\n1. Orphaned Entries (in .bib but never cited in .tex) - REMOVED:")
    if orphans:
        for o in sorted(orphans):
            report.append(f"  - {o}")
    else:
        report.append("  - None")
        
    report.append(f"\n2. Missing/Ambiguous Keys (cited in .tex but missing from .bib):")
    corrections = {}
    if missing:
        for m in sorted(missing):
            # Try to find a close match in existing bib_keys
            close_bib = difflib.get_close_matches(m, bib_keys, n=1, cutoff=0.6)
            # Try to find a match in PDFs
            close_pdf = difflib.get_close_matches(m, pdfs, n=1, cutoff=0.4)
            
            report.append(f"  - {m}")
            if close_bib:
                report.append(f"      -> Best bib match: {close_bib[0]}")
                corrections[m] = close_bib[0]
            elif close_pdf:
                report.append(f"      -> Found related PDF: {close_pdf[0]}")
            else:
                report.append(f"      -> No close match found")
    else:
        report.append("  - None! All citations match perfectly.")
        
    # Write report
    with open('citation_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
        
    # If we have orphans to remove or matches are perfect, write new bib
    # We will only keep keys that are ACTUALLY cited
    write_bib('rujukan_clean.bib', bib_entries, tex_keys.intersection(bib_keys))
    print("Done! See citation_report.txt")

if __name__ == '__main__':
    main()
