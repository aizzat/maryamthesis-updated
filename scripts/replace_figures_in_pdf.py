import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json

# Paths
pdf_path = 'UMP Template.pdf'
output_pdf = 'UMP Template - improved figures.pdf'
figures_dir = Path('figures')

# Load original PDF
doc = fitz.open(pdf_path)
total_pages = len(doc)

print(f"Original PDF: {total_pages} pages")

# Figure pages to replace (0-indexed): pages 26, 27, 30, 36 (shown as 27, 28, 31, 37 in viewer)
# We'll extract the exact locations from inventory
figure_locations = [
    {'original_page': 26, 'figure_name': 'Figure 2.1', 'title': 'System Overview of UGV', 'image_file': 'figure_2_1_system_overview.png'},
    {'original_page': 27, 'figure_name': 'Figure 2.2', 'title': 'Path Planning: 2D vs 2.5D', 'image_file': 'figure_2_2_path_planning.png'},
    {'original_page': 30, 'figure_name': 'Figure 2.3', 'title': '3D Environment Modeling Results', 'image_file': 'figure_2_3_environment_modeling.png'},
    {'original_page': 36, 'figure_name': 'Figure 2.4', 'title': 'Path Smoothing: Grid-Based vs B-Spline', 'image_file': 'figure_2_4_path_smoothing.png'},
]

# Create output document by processing pages
output_doc = fitz.open()
page_mapping = {}
new_page_count = 0

for page_num in range(total_pages):
    # Check if this is a figure page to replace
    figure_info = next((f for f in figure_locations if f['original_page'] == page_num), None)
    
    if figure_info:
        # Create a new page for the improved figure
        new_page = output_doc.new_page(width=612, height=792)  # Letter size
        
        # Add figure
        image_path = figures_dir / figure_info['image_file']
        if image_path.exists():
            rect = fitz.Rect(50, 50, 550, 550)
            new_page.insert_image(rect, filename=str(image_path))
            
            # Add caption
            caption_y = 570
            caption = f"{figure_info['figure_name']}: {figure_info['title']}"
            new_page.insert_text((50, caption_y), caption, fontsize=11, color=(0, 0, 0))
            
            print(f"✓ Replaced {figure_info['figure_name']} (was page {page_num + 1})")
            page_mapping[page_num] = new_page_count
            new_page_count += 1
        else:
            print(f"✗ Warning: Image not found for {figure_info['figure_name']}")
            # Copy original page if image not found
            output_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            new_page_count += 1
    else:
        # Copy original page as-is
        output_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        page_mapping[page_num] = new_page_count
        new_page_count += 1

# Save output document
output_doc.save(output_pdf)
output_doc.close()
doc.close()

print(f"\n✓ PDF saved: {output_pdf}")
print(f"  Original pages: {total_pages}")
print(f"  New pages: {new_page_count}")

# Create mapping report
mapping_report = {
    'timestamp': __import__('datetime').datetime.now().isoformat(),
    'original_pdf': pdf_path,
    'output_pdf': output_pdf,
    'total_figures_replaced': len(figure_locations),
    'figures': [
        {
            'name': f['figure_name'],
            'original_page': f['original_page'] + 1,  # Convert to 1-indexed
            'title': f['title'],
            'svg_file': f['image_file'].replace('.png', '.svg'),
            'png_file': f['image_file'],
        }
        for f in figure_locations
    ]
}

mapping_json = 'figures_replacement_mapping.json'
with open(mapping_json, 'w') as f:
    json.dump(mapping_report, f, indent=2)

print(f"✓ Mapping report saved: {mapping_json}")

# Summary
print("\n" + "="*60)
print("FIGURE REPLACEMENT SUMMARY")
print("="*60)
for fig in figure_locations:
    print(f"{fig['figure_name']}: {fig['title']}")
    print(f"  → SVG: figures/{fig['image_file'].replace('.png', '.svg')}")
    print(f"  → PNG: figures/{fig['image_file']}")
