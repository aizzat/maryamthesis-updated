import fitz
import re
from pathlib import Path
import json

PDF = 'UMP Template.pdf'
BIB_CLEAN = Path('bibliography_cleaned.txt')
REPORT = Path('citation_match_report.txt')
UNMATCHED = Path('unmatched_citations.json')

# Load cleaned bibliography
if not BIB_CLEAN.exists():
    raise SystemExit(f"Cleaned bibliography not found: {BIB_CLEAN}")

bib_text = BIB_CLEAN.read_text(encoding='utf-8')
# Split into paragraphs
paras = [p.strip() for p in re.split(r'\n\s*\n', bib_text) if p.strip()]

# Build bibliography map: (surname, year) -> index
year_re = re.compile(r'\b(19|20)\d{2}\b')

bib_map = {}
for i, p in enumerate(paras, start=1):
    # find first year
    m = year_re.search(p)
    year = m.group(0) if m else None
    # guess surname: take text up to first comma
    first_part = p.split(',')[0]
    # if first_part contains 'REFERENCES' at start, remove it
    first_part = re.sub(r'^(REFERENCES)\b', '', first_part, flags=re.IGNORECASE).strip()
    # handle cases like 'Emmi & Gonzalez-de Santos' -> take first token before '&' or 'and'
    first_part = re.split(r'\band\b|&', first_part, flags=re.IGNORECASE)[0].strip()
    surname = first_part.split()[-1] if first_part else ''
    key = (surname.lower(), year) if surname and year else None
    if key:
        bib_map[key] = {'index': i, 'paragraph': p}

# Extract in-text author-year citations from PDF
doc = fitz.open(PDF)
pages_text = [doc[i].get_text('text') for i in range(len(doc))]
doc.close()
text_all = '\n'.join(pages_text)
# pattern for parenthetical citations
pat = re.compile(r'\(([^()]{2,300}?\d{4}[^()]*)\)')

intext_raw = []
for m in pat.finditer(text_all):
    intext_raw.append(m.group(1).strip())

# Expand multiple citations separated by semicolon
intext_items = []
for raw in intext_raw:
    parts = [p.strip() for p in re.split(r';', raw) if p.strip()]
    for part in parts:
        # remove trailing phrases like 'et al.' and keep year
        intext_items.append(part)

# Normalize each in-text item to (surname, year)
intext_keys = []
for item in intext_items:
    m = year_re.search(item)
    if not m:
        continue
    year = m.group(0)
    before = item[:m.start()]
    # remove commas at end
    before = before.strip().rstrip(',')
    # if contains 'et al.' remove it
    before = re.sub(r'et al\.?', '', before, flags=re.IGNORECASE).strip()
    # split by '&' or 'and'
    before = re.split(r'\band\b|&', before, flags=re.IGNORECASE)[0].strip()
    # take last token as surname
    surname = before.split()[-1] if before else ''
    if surname:
        intext_keys.append((surname.lower(), year))

# Match in-text keys to bib_map
matches = {}
unmatched = []
for key in intext_keys:
    if key in bib_map:
        matches.setdefault(key, []).append(bib_map[key]['index'])
    else:
        # try fuzzy search: any para containing year and surname substring
        sname, yr = key
        found = None
        for bk, val in bib_map.items():
            if val and yr == bk[1] and (sname in bk[0] or bk[0] in sname):
                found = val['index']
                break
        if found:
            matches.setdefault(key, []).append(found)
        else:
            unmatched.append({'surname': sname, 'year': yr})

# Find uncited bibliography entries
cited_bib_indices = set()
for vals in matches.values():
    cited_bib_indices.update(vals)
uncited = [ {'index': info['index'], 'paragraph': info['paragraph']} for k, info in bib_map.items() if info['index'] not in cited_bib_indices ]

# Write report
with REPORT.open('w', encoding='utf-8') as f:
    f.write('Citation Matching Report\n')
    f.write('========================\n\n')
    f.write(f'Total in-text citation items extracted: {len(intext_items)}\n')
    f.write(f'Total bibliography entries parsed: {len(paras)}\n\n')
    f.write('Matched citations (sample):\n')
    for k, vals in list(matches.items())[:50]:
        f.write(f' - {k[0].title()}, {k[1]} -> bib entries: {vals}\n')
    f.write('\nUnmatched in-text citations (surname,year):\n')
    for u in unmatched:
        f.write(f" - {u['surname']},{u['year']}\n")
    f.write('\nUncited bibliography entries (sample up to 20):\n')
    for u in uncited[:20]:
        f.write(f" - bib#{u['index']}: {u['paragraph'][:140]}\n")

# Save unmatched JSON
UNMATCHED.write_text(json.dumps({'unmatched': unmatched, 'uncited_bib': uncited}, indent=2, ensure_ascii=False), encoding='utf-8')

print(f'Report written to {REPORT}')
print(f'Unmatched JSON written to {UNMATCHED}')
