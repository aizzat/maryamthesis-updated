import os
import re
import urllib.request
import urllib.parse
import json
import glob

# 1. Parse rujukan.bib
bib_file = 'rujukan.bib'
with open(bib_file, 'r', encoding='utf-8') as f:
    bib_content = f.read()

entries = {}
entry_pattern = re.compile(r'@\w+\{([^,]+),\s*(.*?)(?=\n@\w+\{|\Z)', re.DOTALL)
for match in entry_pattern.finditer(bib_content):
    ref_id = match.group(1).strip()
    body = match.group(2)
    title_match = re.search(r'Title\s*=\s*[\{"](.*?)(?:[\}"]\s*,|[\}"]\s*$)', body, re.IGNORECASE | re.DOTALL)
    author_match = re.search(r'Author\s*=\s*[\{"](.*?)(?:[\}"]\s*,|[\}"]\s*$)', body, re.IGNORECASE | re.DOTALL)
    
    title = title_match.group(1).replace('\n', ' ').strip() if title_match else ''
    title = title.replace('{', '').replace('}', '')
    author = author_match.group(1).replace('\n', ' ').strip() if author_match else ''
    author = author.replace('{', '').replace('}', '')
    
    entries[ref_id] = {'title': title, 'author': author, 'citations': []}

# 2. Scan for citations in .tex files
tex_dir = '.'
tex_files = glob.glob(os.path.join(tex_dir, '**/*.tex'), recursive=True)

for t_file in tex_files:
    if 'rujukan' in t_file or 'references' in t_file:
        continue
    rel_path = os.path.relpath(t_file, tex_dir)
    with open(t_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if r'\cite' in line:
            cites = re.findall(r'\\cite[a-zA-Z]*(?:\[.*?\])?\{([^}]+)\}', line)
            for cite_group in cites:
                for cite_key in cite_group.split(','):
                    cite_key = cite_key.strip()
                    if cite_key in entries:
                        context = line.strip()
                        if len(context) > 150:
                            idx = context.find(cite_key)
                            start = max(0, idx - 75)
                            end = min(len(context), idx + 75)
                            context = "..." + context[start:end] + "..."
                        entries[cite_key]['citations'].append(f"**{rel_path}**: `{context}`")

# 3. Verify via CrossRef and assess relevance
md_lines = ["# Reference Verification Summary\n"]
md_lines.append("This table checks the references against the CrossRef API to verify online existence, and extracts their exact citation contexts from the thesis.\n")
md_lines.append("| Ref ID | Title | Exists Online? | Relevant? | Where Cited & Context |")
md_lines.append("|---|---|---|---|---|")

def check_crossref(title, author):
    if not title: return "No Title Provided"
    first_author = author.split('and')[0].strip().split()[-1] if author else ""
    query = urllib.parse.quote(title)
    author_query = f"&query.author={urllib.parse.quote(first_author)}" if first_author else ""
    url = f"https://api.crossref.org/works?query.title={query}{author_query}&select=title,author,DOI&rows=1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ThesisChecker/1.0 (mailto:test@example.com)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            items = data.get('message', {}).get('items', [])
            if items:
                ret_title = items[0].get('title', [''])[0]
                if ret_title.lower()[:20] == title.lower()[:20]:
                    return "Yes"
                else:
                    return f"Maybe (Found: {ret_title[:30]}...)"
            return "No"
    except Exception as e:
        return f"API Error"

topic_keywords = ['terrain', 'path', 'plan', 'navigat', 'ugv', 'autonomous', 'robot', 'astar', 'a-star', 'a*', 'spline', 'off-road', '2.5d', 'grid', 'map', 'smooth']

count = 0
for ref_id, info in entries.items():
    title = info['title']
    author = info['author']
    
    exists = check_crossref(title, author)
    
    title_lower = title.lower()
    relevant = "No (Manual Check Required)"
    for kw in topic_keywords:
        if kw in title_lower:
            relevant = "Yes"
            break
            
    cites = "<br><br>".join(info['citations']) if info['citations'] else "*Not cited in text*"
    
    md_lines.append(f"| {ref_id} | {title} | {exists} | {relevant} | {cites} |")
    count += 1
    if count % 10 == 0:
        print(f"Processed {count}/{len(entries)} references...")

with open('/Users/aizzat/.gemini/antigravity-ide/brain/704978a7-50d8-4bb2-9889-b86028888fcc/reference_check.md', 'w') as f:
    f.write("\n".join(md_lines))
print("Done writing artifact.")
