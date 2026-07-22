import fitz
import re
from pathlib import Path

PDF = 'UMP Template.pdf'
OUT_RAW = Path('bibliography_raw.txt')
OUT_CLEAN = Path('bibliography_cleaned.txt')

# Open PDF and find bibliography start
doc = fitz.open(PDF)
start_idx = None
header_pattern = re.compile(r'^(References|Bibliography)\b', re.IGNORECASE)
appendix_pattern = re.compile(r'^(APPENDIX|APPENDICES)\b', re.IGNORECASE)

for i in range(len(doc)):
    text = doc[i].get_text('text')
    for line in text.splitlines()[:8]:
        if header_pattern.search(line.strip()):
            start_idx = i
            break
    if start_idx is not None:
        break

if start_idx is None:
    print('Bibliography start not found')
    doc.close()
    raise SystemExit(1)

# Find end (appendix) if present
end_idx = len(doc)
for j in range(start_idx, len(doc)):
    text = doc[j].get_text('text')
    for line in text.splitlines()[:4]:
        if appendix_pattern.search(line.strip()):
            end_idx = j
            break
    if end_idx != len(doc):
        break

# Extract raw text
pages = [doc[p].get_text('text') for p in range(start_idx, end_idx)]
doc.close()
raw_text = '\n\n'.join(pages)
OUT_RAW.write_text(raw_text, encoding='utf-8')
print(f'Wrote raw bibliography to {OUT_RAW} (pages {start_idx+1}..{end_idx})')

# Clean text heuristics:
# 1) Remove hyphenation at line ends: 'exam-\nple' -> 'example'
# 2) Replace multiple newlines with paragraph separators
# 3) Join lines within paragraphs: replace single newlines with space

t = raw_text
# normalize common unicode hyphen-like chars
t = t.replace('\u2010', '-')
# remove hyphen at line ends
t = re.sub(r'-\n\s*', '', t)
# replace CRLF/line endings
# split into paragraphs by double-newline groups
paras = [p.strip() for p in re.split(r'\n\s*\n', t) if p.strip()]
# join internal single-newline breaks
clean_paras = []
for p in paras:
    # replace internal newlines with space
    p2 = re.sub(r'\n+', ' ', p)
    # collapse multiple spaces
    p2 = re.sub(r'\s+', ' ', p2).strip()
    clean_paras.append(p2)

clean_text = '\n\n'.join(clean_paras)
OUT_CLEAN.write_text(clean_text, encoding='utf-8')
print(f'Wrote cleaned bibliography to {OUT_CLEAN} with {len(clean_paras)} paragraphs')
