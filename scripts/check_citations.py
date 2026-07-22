import fitz
import re
from collections import defaultdict

PDF = 'UMP Template.pdf'

def extract_text_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = [doc[i].get_text("text") for i in range(len(doc))]
    doc.close()
    return pages

def find_intext_citations(pages):
    cit_nums = defaultdict(list)
    cit_auth = defaultdict(list)
    num_pattern = re.compile(r"\[(\d{1,3})\]")
    author_year_pattern = re.compile(r"\(([^()]{2,100}?\,\s*\d{4})\)")
    for i, text in enumerate(pages):
        for m in num_pattern.finditer(text):
            cit_nums[int(m.group(1))].append(i+1)
        for m in author_year_pattern.finditer(text):
            cit_auth[m.group(1)].append(i+1)
    return cit_nums, cit_auth

def find_bibliography(pages):
    # Find page index where References/Bibliography starts
    start_idx = None
    header_pattern = re.compile(r'^(References|Bibliography)\b', re.IGNORECASE)
    for i, text in enumerate(pages):
        lines = text.splitlines()
        for line in lines[:5]:
            if header_pattern.search(line.strip()):
                start_idx = i
                break
        if start_idx is not None:
            break

    if start_idx is None:
        return None, None

    # Collect bibliography text from start_idx until APPENDIX or end
    end_idx = len(pages)
    appendix_pattern = re.compile(r'^(APPENDIX|APPENDICES)\b', re.IGNORECASE)
    for j in range(start_idx, len(pages)):
        first_lines = pages[j].splitlines()
        for line in first_lines[:3]:
            if appendix_pattern.search(line.strip()):
                end_idx = j
                break
        if end_idx != len(pages):
            break

    bib_text = "\n".join(pages[start_idx:end_idx])

    # Try numeric entries like '1. Author...' or '[1] Author...'
    numeric_entry_pattern = re.compile(r'^(?:\[?(\d{1,3})\]?\.?\s+)(.+)$', re.MULTILINE)
    entries = {}
    for m in numeric_entry_pattern.finditer(bib_text):
        try:
            num = int(m.group(1))
            entries[num] = m.group(2).strip()
        except:
            continue

    # If no numeric entries found, fallback to heuristic paragraph extraction
    if not entries:
        # Try to split into paragraphs by double-newline (may work for PDF text)
        paras = [p.strip() for p in re.split(r'\n\s*\n', bib_text) if p.strip()]
        # If still too few paragraphs, fallback to lines grouped by line length
        if len(paras) < 3:
            lines = [l.rstrip() for l in bib_text.splitlines()]
            paras = []
            cur = []
            for l in lines:
                if l.strip() == '':
                    if cur:
                        paras.append(' '.join(cur))
                        cur = []
                else:
                    cur.append(l.strip())
            if cur:
                paras.append(' '.join(cur))
        entries = {i+1: p for i, p in enumerate(paras)}

    return start_idx+1, entries

def main():
    pages = extract_text_pages(PDF)
    cit_nums, cit_auth = find_intext_citations(pages)
    bib_start_page, bib_entries = find_bibliography(pages)

    print(f"Total pages: {len(pages)}")
    print(f"Bibliography starts on page: {bib_start_page if bib_start_page else 'NOT FOUND'}")
    print('\nIn-text numeric citations found:')
    if cit_nums:
        for num in sorted(cit_nums.keys()):
            print(f"  [{num}] on pages: {', '.join(map(str, cit_nums[num]))}")
    else:
        print('  None')

    print('\nIn-text author-year citations found:')
    if cit_auth:
        for auth in sorted(cit_auth.keys()):
            print(f"  ({auth}) on pages: {', '.join(map(str, cit_auth[auth]))}")
    else:
        print('  None')

    print('\nBibliography entries extracted (first 120 chars):')
    if bib_entries:
        for k in sorted(bib_entries.keys()):
            snippet = bib_entries[k][:120].replace('\n', ' ')
            print(f"  {k}: {snippet}")
    else:
        print('  None')

    # Heuristic matching: extract (first author surname, year) pairs from bibliography
    bib_pairs = {}
    year_pattern = re.compile(r'\b(19|20)\d{2}\b')
    for k, text in (bib_entries or {}).items():
        yrs = year_pattern.findall(text)
        years = year_pattern.findall(text)
        m = year_pattern.search(text)
        year = m.group(0) if m else None
        # Take first token before comma as possible surname
        first_part = text.split(',')[0]
        surname = first_part.split()[-1] if first_part else ''
        if surname and year:
            key = f"{surname},{year}"
            bib_pairs[key.lower()] = (k, text)

    # Normalize in-text author-year citations to (surname, year)
    def normalize_auth_key(s):
        # s may contain multiple citations separated by semicolon
        s = s.replace('\n',' ').strip()
        # pick first author-year pair inside
        # pattern like 'Surname, X., et al., 2021' or 'Surname & Other, 2021'
        # find year
        m = year_pattern.search(s)
        if not m:
            return None
        year = m.group(0)
        # find first capitalized token before year
        before = s[:m.start()]
        # take last word token before comma or semicolon
        tokens = re.split('[,;]', before)
        first = tokens[0].strip()
        surname = first.split()[-1] if first else ''
        if surname:
            return f"{surname},{year}".lower()
        return None

    intext_keys = set()
    for auth in cit_auth.keys():
        k = normalize_auth_key(auth)
        if k:
            intext_keys.add(k)

    # Compare
    missing = [k for k in sorted(intext_keys) if k not in bib_pairs]
    uncited = [v for k,v in bib_pairs.items() if k not in intext_keys]

    print('\nHeuristic match results:')
    if missing:
        print('  In-text author-year citations not found in bibliography (heuristic):')
        for m in missing:
            print(f"    - {m}")
    else:
        print('  All in-text author-year citations appear to have bibliography matches (heuristic)')

    if uncited:
        print(f"  Bibliography entries not cited in-text (sample up to 10): {len(uncited)} total")
        for i, (idx, txt) in enumerate(uncited[:10]):
            snippet = txt[:80].replace('\n', ' ')
            print(f"    - bib#{idx}: {snippet}")
    else:
        print('  No uncited bibliography entries found (heuristic)')

    # Compare numeric citations to bibliography
    if bib_entries and cit_nums:
        cited_set = set(cit_nums.keys())
        bib_set = set(bib_entries.keys())
        missing_in_bib = sorted(cited_set - bib_set)
        uncited_in_bib = sorted(bib_set - cited_set)
        print('\nComparison:')
        if missing_in_bib:
            print(f"  Cited in-text but missing from bibliography: {missing_in_bib}")
        else:
            print('  All numeric in-text citations have bibliography entries')
        if uncited_in_bib:
            print(f"  Bibliography entries not cited in-text: {uncited_in_bib[:20]}{'...' if len(uncited_in_bib)>20 else ''}")
        else:
            print('  No uncited bibliography entries')

if __name__ == '__main__':
    main()
