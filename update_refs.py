import re
import os
import glob
from collections import defaultdict

def generate_new_keys():
    with open('rujukan.bib', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all entries: @type{key, ... }
    # Since bibtex can be nested, regex might be tricky, but let's assume standard formatting.
    # Entries look like @article{Ref10, \n  Author = {...}, \n ... \n}
    
    # We will split by '@' to get each entry
    entries = content.split('\n@')
    
    mapping = {}
    new_keys_seen = defaultdict(int)
    
    for i, entry in enumerate(entries):
        if not entry.strip():
            continue
            
        # The first chunk before splitting was just comments if it didn't start with @
        if i == 0 and not content.startswith('@'):
            continue
            
        # extract key
        key_match = re.search(r'^[a-zA-Z]+{([^,]+),', entry, re.IGNORECASE)
        if not key_match:
            continue
        old_key = key_match.group(1).strip()
        
        if not old_key.startswith('Ref'): # Only change Ref* if needed, or all. Let's do all or specifically Ref*
            # Actually, user wants all references changed.
            pass
            
        # Extract Author
        author_match = re.search(r'Author\s*=\s*{([^{}]*(?:{[^{}]*}[^{}]*)*)}', entry, re.IGNORECASE)
        if not author_match:
            # fallback
            author_match = re.search(r'Author\s*=\s*{([^}]+)}', entry, re.IGNORECASE)
        
        # Extract Year
        year_match = re.search(r'Year\s*=\s*{([^}]+)}', entry, re.IGNORECASE)
        
        # Extract Title
        title_match = re.search(r'Title\s*=\s*{([^{}]*(?:{[^{}]*}[^{}]*)*)}', entry, re.IGNORECASE)
        if not title_match:
            title_match = re.search(r'Title\s*=\s*{([^}]+)}', entry, re.IGNORECASE)
            
        author = author_match.group(1) if author_match else "Unknown"
        year = year_match.group(1) if year_match else "XXXX"
        title = title_match.group(1) if title_match else "title"
        
        # Process Author: get first author's last name
        first_author = author.split(' and ')[0].strip()
        if ',' in first_author:
            last_name = first_author.split(',')[0].strip()
        else:
            last_name = first_author.split(' ')[-1].strip()
            
        # Remove non-alphanumeric from last name
        last_name = re.sub(r'[^a-zA-Z0-9]', '', last_name)
        
        # Process Year
        year = re.sub(r'[^0-9]', '', year)
        if not year:
            year = "XXXX"
            
        # Process Title: remove braces, lowercase, keep alphanumeric and spaces
        title_clean = title.replace('{', '').replace('}', '')
        title_clean = re.sub(r'[^a-zA-Z0-9\s\.-]', '', title_clean).strip()
        # Get first 1-3 words
        words = [w for w in title_clean.split() if w.lower() not in ('a', 'an', 'the', 'in', 'on', 'of', 'for', 'and')]
        short_title = "".join(words[:2]).lower() # combine first two meaningful words
        # Remove any remaining punctuation from short_title
        short_title = re.sub(r'[^a-z0-9]', '', short_title)
        
        if not short_title:
            short_title = "ref"
            
        new_key_base = f"{last_name}_{year}_{short_title}"
        
        if new_keys_seen[new_key_base] > 0:
            new_key = f"{new_key_base}_{chr(96 + new_keys_seen[new_key_base])}" # append a, b, c...
        else:
            new_key = new_key_base
            
        new_keys_seen[new_key_base] += 1
        
        mapping[old_key] = new_key

    return mapping

def update_files(mapping):
    # 1. Update rujukan.bib
    with open('rujukan.bib', 'r', encoding='utf-8') as f:
        bib_content = f.read()
        
    for old_key, new_key in mapping.items():
        # Replace the key definition in bib file
        bib_content = re.sub(r'(@[a-zA-Z]+{)' + re.escape(old_key) + r'(,)', r'\g<1>' + new_key + r'\g<2>', bib_content, count=1, flags=re.IGNORECASE)
        
    with open('rujukan.bib', 'w', encoding='utf-8') as f:
        f.write(bib_content)
        
    # 2. Update .tex files
    tex_files = glob.glob('**/*.tex', recursive=True)
    for tex_file in tex_files:
        with open(tex_file, 'r', encoding='utf-8') as f:
            tex_content = f.read()
            
        original_content = tex_content
        for old_key, new_key in mapping.items():
            # \b matches word boundary. 
            # We want to replace old_key with new_key only as a whole word
            # since old_keys like Ref1 could be inside Ref10
            # We'll use a regex that ensures it's surrounded by non-word chars, but wait, 
            # Ref1 is a word. So \bRef1\b is perfect.
            tex_content = re.sub(r'\b' + re.escape(old_key) + r'\b', new_key, tex_content)
            
        if tex_content != original_content:
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(tex_content)
            print(f"Updated {tex_file}")

if __name__ == "__main__":
    mapping = generate_new_keys()
    print(f"Generated {len(mapping)} new keys. Applying...")
    for k, v in list(mapping.items())[:5]:
        print(f"  {k} -> {v}")
    update_files(mapping)
    print("Done!")
