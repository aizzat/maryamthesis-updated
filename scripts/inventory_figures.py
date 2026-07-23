import fitz
from pathlib import Path
import json

pdf_path = Path('UMP Template.pdf')
doc = fitz.open(pdf_path)

figures = []
for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text()
    images = page.get_images(full=True)
    
    if images or 'figure' in text.lower():
        figures.append({
            'page': pno + 1,
            'text_preview': text[:300] if text else '(no text)',
            'image_count': len(images)
        })

print(f"Total pages: {len(doc)}")
print(f"Pages with figures/images: {len(figures)}\n")
for i, fig in enumerate(figures, 1):
    print(f"Figure {i}: Page {fig['page']}, Images: {fig['image_count']}")
    print(f"  Text: {fig['text_preview'][:80]}...")
    print()

# save as JSON for reference
with open('figures_inventory.json', 'w') as f:
    json.dump(figures, f, indent=2)

doc.close()
