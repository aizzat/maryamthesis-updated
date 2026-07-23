from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from pathlib import Path

figures_dir = Path('figures')

# Convert all SVG files to PNG
svg_files = sorted(figures_dir.glob('figure_2_*.svg'))

print(f"Converting {len(svg_files)} SVG files to PNG (Windows-compatible)...\n")

for svg_file in svg_files:
    png_file = svg_file.with_suffix('.png')
    
    try:
        # Convert SVG to reportlab drawing
        drawing = svg2rlg(str(svg_file))
        if drawing:
            # Render to PNG
            renderPM.drawToFile(drawing, str(png_file), fmt='PNG')
            print(f"✓ {svg_file.name} → {png_file.name}")
        else:
            print(f"✗ Failed to parse {svg_file.name}")
    except Exception as e:
        print(f"✗ Error converting {svg_file.name}: {type(e).__name__}: {e}")

print("\n✅ PNG conversion complete!")
