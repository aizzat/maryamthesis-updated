import re
import json
from pathlib import Path
import fitz

PDF = 'UMP Template.pdf'
BIB_CLEAN = Path('bibliography_cleaned.txt')
REPORT = Path('citation_match_report_improved.txt')
UNMATCHED = Path('unmatched_citations_improved.json')

text = BIB_CLEAN.read_text(encoding='utf-8')
# Find candidate positions for entries using '(<year>)' occurrences
year_pat = re.compile(r'\(\s*(1[89]\d{2}|20\d{2})\s*\)')
matches = list(year_pat.finditer(text))

entries = []
if not matches:
    # fallback: split by double newlines
    entries = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
else:
    for i, m in enumerate(matches):
        start = m.start()
        # extend backward to include authors starting position
        # find start of line or previous double-space
        prev_cut = text.rfind('\n\n', 0, start)
        if prev_cut == -1:
            prev_cut = 0
        else:
            prev_cut += 2
        # entry ends before next match start
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        entry = text[prev_cut:end].strip()
        # clean leading 'REFERENCES' if present
        entry = re.sub(r'^REFERENCES\s*', '', entry, flags=re.IGNORECASE).strip()
        if entry:
            entries.append(entry)

# Post-process entries: split if an entry contains multiple occurrences of year pattern (rare)
processed = []
for e in entries:
    sub = [s.strip() for s in re.split(r'(?=\(\s*(1[89]\d{2}|20\d{2})\s*\))', e) if s.strip()]
    if len(sub) > 1:
        # recombine pairs: year token + following text
        combined = []
        i = 0
        while i < len(sub):
            if year_pat.match(sub[i]):
                if i+1 < len(sub):
                    combined.append((sub[i] + sub[i+1]).strip())
                    i += 2
                else:
                    combined.append(sub[i].strip())
                    i += 1
            else:
                # find next year
                j = i+1
                s = sub[i]
                while j < len(sub) and not year_pat.match(sub[j]):
                    s += ' ' + sub[j]
                    j += 1
                combined.append(s.strip())
                i = j
        for c in combined:
            processed.append(c)
    else:
        processed.append(e)

# Further split by recognizing 'https://' DOIs that often end entries
final_entries = []
for e in processed:
    parts = re.split(r'(?<=\.\s)(?=[A-Z][a-z]{2,}\s*,)', e)
    if len(parts) > 1:
        for p in parts:
            if p.strip():
                final_entries.append(p.strip())
    else:
        final_entries.append(e.strip())

# Build bibliography map with (surname, year)
year_re = re.compile(r'(1[89]\d{2}|20\d{2})')
bib_map = {}
for idx, entry in enumerate(final_entries, start=1):
    m = year_re.search(entry)
    year = m.group(0) if m else None
    first_part = entry.split(',')[0]
    first_part = re.sub(r'^(REFERENCES)\b', '', first_part, flags=re.IGNORECASE).strip()
    first_part = re.split(r'\band\b|&', first_part, flags=re.IGNORECASE)[0].strip()
    surname = first_part.split()[-1] if first_part else ''
    if surname and year:
        key = (surname.lower(), year)
        bib_map[key] = {'index': idx, 'entry': entry}

# Extract in-text citations
doc = fitz.open(PDF)
pages_text = [doc[i].get_text('text') for i in range(len(doc))]
doc.close()
text_all = '\n'.join(pages_text)
pat = re.compile(r'\(([^()]{2,300}?\d{4}[^()]*)\)')

intext_raw = []
for m in pat.finditer(text_all):
    intext_raw.append(m.group(1).strip())

intext_items = []
for raw in intext_raw:
    parts = [p.strip() for p in re.split(r';', raw) if p.strip()]
    for part in parts:
        intext_items.append(part)

# normalize in-text to (surname, year)
intext_keys = []
for item in intext_items:
    m = year_re.search(item)
    if not m:
        continue
    year = m.group(0)
    before = item[:m.start()].strip().rstrip(',')
    before = re.sub(r'et al\.?', '', before, flags=re.IGNORECASE).strip()
    before = re.split(r'\band\b|&', before, flags=re.IGNORECASE)[0].strip()
    surname = before.split()[-1] if before else ''
    if surname:
        intext_keys.append((surname.lower(), year))

# Match
matches = {}
unmatched = []
for key in intext_keys:
    if key in bib_map:
        matches.setdefault(key, []).append(bib_map[key]['index'])
    else:
        # fuzzy: search paragraphs containing year and surname substring
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

cited_indices = set()
for vals in matches.values():
    cited_indices.update(vals)
uncited = [ {'index': idx, 'entry': entry} for idx, entry in enumerate(final_entries, start=1) if idx not in cited_indices ]

# Write outputs
REPORT.write_text('Citation Matching Report (Improved)\n', encoding='utf-8')
with REPORT.open('a', encoding='utf-8') as f:
    f.write(f'Total in-text citation items: {len(intext_items)}\n')
    f.write(f'Total bibliography entries parsed (improved): {len(final_entries)}\n\n')
    f.write('Sample matched citations:\n')
    for k, vals in list(matches.items())[:60]:
        f.write(f' - {k[0].title()}, {k[1]} -> bib entries: {vals}\n')
    f.write('\nUnmatched in-text citations (surname,year):\n')
    for u in unmatched:
        f.write(f" - {u['surname']},{u['year']}\n")
    f.write('\nUncited bibliography entries (sample up to 30):\n')
    for u in uncited[:30]:
        f.write(f" - bib#{u['index']}: {u['entry'][:140]}\n")

UNMATCHED.write_text(json.dumps({'unmatched': unmatched, 'uncited_bib': uncited}, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Wrote improved report to {REPORT} and unmatched JSON to {UNMATCHED}')
