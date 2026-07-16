import re
import glob
import os

bib_content = open("rujukan.bib").read()

# Pattern to extract block of entry
pattern = re.compile(r'(@\w+\s*\{)([^,]+)(,\s*.*?\n\})', re.DOTALL)
entries = pattern.findall(bib_content)

seen = {}
mapping = {}
unique_bib = "%% rujukan.bib - Complete Bibliography for Maryam's Master Thesis\n%% Generated: July 2026\n%% All entries correspond to Ref* citation keys used in the LaTeX chapters.\n%% Bibliographic details extracted from actual PDF literature files.\n\n"

for p1, key, p3 in entries:
    norm_body = re.sub(r'\s+', ' ', p3).strip()
    if norm_body in seen:
        mapping[key] = seen[norm_body]
    else:
        seen[norm_body] = key
        unique_bib += f"{p1}{key}{p3}\n\n"

with open("rujukan.bib", "w") as f:
    f.write(unique_bib)

# Now find all .tex files and replace duplicate keys
tex_files = glob.glob("**/*.tex", recursive=True)
for tf in tex_files:
    try:
        with open(tf, "r") as f:
            content = f.read()
            
        modified = False
        for dup, pri in mapping.items():
            # Replace \citep{...,Ref3,...} etc.
            # Using regex to carefully replace whole words
            content_new = re.sub(r'\b' + re.escape(dup) + r'\b', pri, content)
            if content_new != content:
                content = content_new
                modified = True
                
        if modified:
            with open(tf, "w") as f:
                f.write(content)
            print(f"Updated {tf}")
    except Exception as e:
        pass

