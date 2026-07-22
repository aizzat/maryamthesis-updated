import json
from pathlib import Path
p = Path('unmatched_citations_improved.json')
with p.open(encoding='utf-8') as f:
    j = json.load(f)
print('unmatched=', len(j.get('unmatched', [])))
print('uncited_bib=', len(j.get('uncited_bib', [])))
