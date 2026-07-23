import json
p='..\\unmatched_citations_improved.json'
with open(p,encoding='utf-8') as f:
    j=json.load(f)
print('unmatched=',len(j['unmatched']))
print('uncited_bib=',len(j['uncited_bib']))
