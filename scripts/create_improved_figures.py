from pathlib import Path
import fitz
# Will use svg2png later if needed
from PIL import Image, ImageDraw, ImageFont
import io

figures_dir = Path('figures')
figures_dir.mkdir(exist_ok=True)

# Helper: create SVG from string
def save_svg(filename, svg_content):
    path = figures_dir / filename
    path.write_text(svg_content, encoding='utf-8')
    return path

# Helper: convert SVG string to PNG via cairosvg if available, else PIL
def svg_to_png(svg_content, output_path, width=800, height=600):
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=str(output_path), output_width=width, output_height=height)
    except Exception:
        # Fallback: create basic PNG with text
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), "(SVG to PNG conversion not available)", fill='black')
        img.save(output_path, 'PNG')

# Figure 2.1: System Overview of Unmanned Ground Vehicle (Block Diagram)
svg_fig_2_1 = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <style>
    rect { fill: #e8f4f8; stroke: #333; stroke-width: 2; }
    text { font-family: Arial, sans-serif; font-size: 14px; fill: #000; }
    .title { font-size: 18px; font-weight: bold; }
    line { stroke: #333; stroke-width: 2; }
    polygon { fill: none; stroke: #333; stroke-width: 2; }
  </style>
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" class="title">System Overview of Unmanned Ground Vehicle (UGV)</text>
  <!-- Sensing Layer -->
  <rect x="50" y="80" width="150" height="80" rx="5"/>
  <text x="125" y="110" text-anchor="middle">LiDAR</text>
  <text x="125" y="135" text-anchor="middle">Sensors</text>
  <rect x="250" y="80" width="150" height="80" rx="5"/>
  <text x="325" y="110" text-anchor="middle">Camera</text>
  <text x="325" y="135" text-anchor="middle">Vision</text>
  <rect x="450" y="80" width="150" height="80" rx="5"/>
  <text x="525" y="110" text-anchor="middle">IMU/GNSS</text>
  <text x="525" y="135" text-anchor="middle">Localization</text>
  <!-- Processing Layer -->
  <rect x="150" y="220" width="500" height="80" rx="5"/>
  <text x="400" y="255" text-anchor="middle" font-size="16px" font-weight="bold">Path Planning & Navigation System</text>
  <!-- Output Layer -->
  <rect x="50" y="360" width="150" height="80" rx="5"/>
  <text x="125" y="390" text-anchor="middle">Motor</text>
  <text x="125" y="415" text-anchor="middle">Control</text>
  <rect x="250" y="360" width="150" height="80" rx="5"/>
  <text x="325" y="390" text-anchor="middle">Vehicle</text>
  <text x="325" y="415" text-anchor="middle">Dynamics</text>
  <rect x="450" y="360" width="150" height="80" rx="5"/>
  <text x="525" y="390" text-anchor="middle">Trajectory</text>
  <text x="525" y="415" text-anchor="middle">Tracking</text>
  <!-- Connecting arrows -->
  <line x1="125" y1="160" x2="125" y2="220"/>
  <polygon points="125,220 120,210 130,210"/>
  <line x1="325" y1="160" x2="325" y2="220"/>
  <polygon points="325,220 320,210 330,210"/>
  <line x1="525" y1="160" x2="525" y2="220"/>
  <polygon points="525,220 520,210 530,210"/>
  <!-- To output layer -->
  <line x1="125" y1="300" x2="125" y2="360"/>
  <polygon points="125,360 120,350 130,350"/>
  <line x1="325" y1="300" x2="325" y2="360"/>
  <polygon points="325,360 320,350 330,350"/>
  <line x1="525" y1="300" x2="525" y2="360"/>
  <polygon points="525,360 520,350 530,350"/>
  <!-- Legend -->
  <text x="50" y="540" font-size="12px">Input Sensors → Processing → Output Control</text>
</svg>'''

# Figure 2.2: Path Planning Illustration (2D vs 2.5D)
svg_fig_2_2 = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <style>
    rect { fill: #f0f0f0; stroke: #333; stroke-width: 2; }
    circle { fill: #ff6b6b; }
    path { stroke: #0066cc; stroke-width: 3; fill: none; }
    text { font-family: Arial, sans-serif; font-size: 14px; fill: #000; }
    .title { font-size: 18px; font-weight: bold; }
    .label { font-size: 12px; }
  </style>
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" class="title">Path Planning: 2D vs 2.5D Elevation Grid</text>
  <!-- 2D Path Planning -->
  <text x="200" y="70" text-anchor="middle" font-weight="bold">2D Path (Horizontal)</text>
  <rect x="50" y="100" width="300" height="250" rx="5" fill="#e8f4f8"/>
  <circle cx="100" cy="150" r="8"/><!-- Start -->
  <circle cx="300" cy="300" r="8" fill="#00cc00"/><!-- Goal -->
  <!-- 2D path -->
  <path d="M 100 150 L 120 170 L 150 180 L 200 200 L 280 280 L 300 300"/>
  <text x="200" y="380" text-anchor="middle" class="label">Simple Euclidean Path</text>
  <text x="200" y="400" text-anchor="middle" class="label">(No terrain awareness)</text>
  <!-- 2.5D Path Planning -->
  <text x="600" y="70" text-anchor="middle" font-weight="bold">2.5D Path (Terrain-Aware)</text>
  <rect x="450" y="100" width="300" height="250" rx="5" fill="#e8ffe8"/>
  <circle cx="500" cy="150" r="8"/><!-- Start -->
  <circle cx="700" cy="300" r="8" fill="#00cc00"/><!-- Goal -->
  <!-- 2.5D path (with slope indication) -->
  <path d="M 500 150 Q 520 160 550 170 Q 600 190 650 240 Q 680 270 700 300" stroke-dasharray="5,5"/>
  <!-- Elevation contours -->
  <line x1="470" y1="280" x2="730" y2="280" stroke="#999" stroke-dasharray="3,3"/>
  <line x1="470" y1="250" x2="730" y2="250" stroke="#999" stroke-dasharray="3,3"/>
  <line x1="470" y1="220" x2="730" y2="220" stroke="#999" stroke-dasharray="3,3"/>
  <text x="600" y="380" text-anchor="middle" class="label">Slope-Aware Path</text>
  <text x="600" y="400" text-anchor="middle" class="label">(With elevation constraints)</text>
  <!-- Legend -->
  <text x="100" y="480" font-size="12px">● = Start Point</text>
  <text x="100" y="510" font-size="12px">● = Goal Point</text>
</svg>'''

# Figure 2.3: 3D Environment Modeling Results
svg_fig_2_3 = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <style>
    rect { fill: #e8f4f8; stroke: #333; stroke-width: 1; }
    polygon { fill: #b3d9ff; stroke: #0066cc; stroke-width: 1.5; }
    text { font-family: Arial, sans-serif; font-size: 14px; fill: #000; }
    .title { font-size: 18px; font-weight: bold; }
    .label { font-size: 12px; }
  </style>
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" class="title">Real-World 3D Environment Modeling Results</text>
  <!-- Point Cloud Representation -->
  <text x="200" y="80" text-anchor="middle" font-weight="bold">Point Cloud (Raw Data)</text>
  <circle cx="150" cy="150" r="2" fill="#ff6b6b"/>
  <circle cx="160" cy="160" r="2" fill="#ff6b6b"/>
  <circle cx="170" cy="155" r="2" fill="#ff6b6b"/>
  <circle cx="145" cy="170" r="2" fill="#ff6b6b"/>
  <circle cx="155" cy="180" r="2" fill="#ff6b6b"/>
  <circle cx="175" cy="175" r="2" fill="#ff6b6b"/>
  <circle cx="200" cy="140" r="2" fill="#ff6b6b"/>
  <circle cx="210" cy="165" r="2" fill="#ff6b6b"/>
  <circle cx="220" cy="180" r="2" fill="#ff6b6b"/>
  <circle cx="240" cy="150" r="2" fill="#ff6b6b"/>
  <circle cx="250" cy="170" r="2" fill="#ff6b6b"/>
  <!-- 2.5D Elevation Grid -->
  <text x="600" y="80" text-anchor="middle" font-weight="bold">2.5D Elevation Grid</text>
  <rect x="520" y="110" width="30" height="30" fill="#90EE90"/>
  <rect x="550" y="110" width="30" height="30" fill="#7CCD7C"/>
  <rect x="580" y="110" width="30" height="30" fill="#6BB86B"/>
  <rect x="610" y="110" width="30" height="30" fill="#808080"/>
  <rect x="520" y="140" width="30" height="30" fill="#90EE90"/>
  <rect x="550" y="140" width="30" height="30" fill="#90EE90"/>
  <rect x="580" y="140" width="30" height="30" fill="#7CCD7C"/>
  <rect x="610" y="140" width="30" height="30" fill="#696969"/>
  <rect x="520" y="170" width="30" height="30" fill="#90EE90"/>
  <rect x="550" y="170" width="30" height="30" fill="#7CCD7C"/>
  <rect x="580" y="170" width="30" height="30" fill="#7CCD7C"/>
  <rect x="610" y="170" width="30" height="30" fill="#A9A9A9"/>
  <!-- Color scale -->
  <text x="100" y="280" class="label">Sparse 3D Data</text>
  <text x="550" y="280" class="label">Color = Elevation</text>
  <line x1="500" y1="300" x2="750" y2="300" stroke="#999" stroke-width="1"/>
  <rect x="500" y="290" width="20" height="20" fill="#90EE90"/>
  <text x="530" y="305" class="label">Low</text>
  <rect x="580" y="290" width="20" height="20" fill="#7CCD7C"/>
  <text x="610" y="305" class="label">Medium</text>
  <rect x="660" y="290" width="20" height="20" fill="#696969"/>
  <text x="690" y="305" class="label">High</text>
</svg>'''

# Figure 2.4: Path Smoothing Illustration
svg_fig_2_4 = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <style>
    line { stroke: #333; stroke-width: 2; }
    path { stroke: #0066cc; stroke-width: 3; fill: none; }
    circle { fill: #ff6b6b; }
    rect { fill: #f0f0f0; stroke: #333; stroke-width: 1; }
    text { font-family: Arial, sans-serif; font-size: 14px; fill: #000; }
    .title { font-size: 18px; font-weight: bold; }
    .label { font-size: 12px; }
  </style>
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" class="title">Path Smoothing: Grid-Based vs B-Spline Curve</text>
  <!-- Grid -->
  <line x1="50" y1="80" x2="50" y2="380" stroke="#ccc" stroke-width="1"/>
  <line x1="90" y1="80" x2="90" y2="380" stroke="#ccc" stroke-width="1"/>
  <line x1="130" y1="80" x2="130" y2="380" stroke="#ccc" stroke-width="1"/>
  <line x1="170" y1="80" x2="170" y2="380" stroke="#ccc" stroke-width="1"/>
  <line x1="210" y1="80" x2="210" y2="380" stroke="#ccc" stroke-width="1"/>
  <line x1="250" y1="80" x2="250" y2="380" stroke="#ccc" stroke-width="1"/>
  <line x1="50" y1="80" x2="250" y2="80" stroke="#ccc" stroke-width="1"/>
  <line x1="50" y1="120" x2="250" y2="120" stroke="#ccc" stroke-width="1"/>
  <line x1="50" y1="160" x2="250" y2="160" stroke="#ccc" stroke-width="1"/>
  <line x1="50" y1="200" x2="250" y2="200" stroke="#ccc" stroke-width="1"/>
  <line x1="50" y1="240" x2="250" y2="240" stroke="#ccc" stroke-width="1"/>
  <line x1="50" y1="280" x2="250" y2="280" stroke="#ccc" stroke-width="1"/>
  <line x1="50" y1="320" x2="250" y2="320" stroke="#ccc" stroke-width="1"/>
  <line x1="50" y1="360" x2="250" y2="360" stroke="#ccc" stroke-width="1"/>
  <!-- Discrete path (angular) -->
  <text x="150" y="420" text-anchor="middle" font-weight="bold">Discrete Grid Path</text>
  <path d="M 70 100 L 90 120 L 110 140 L 130 160 L 150 180 L 170 200 L 190 220 L 210 240 L 230 260" stroke="#ff6b6b" stroke-width="2.5" fill="none"/>
  <!-- Waypoints -->
  <circle cx="70" cy="100" r="3" fill="#ff6b6b"/>
  <circle cx="230" cy="260" r="3" fill="#00cc00"/>
  <!-- Smooth path (B-spline) -->
  <text x="550" y="420" text-anchor="middle" font-weight="bold">Smoothed B-Spline Path</text>
  <path d="M 500 100 Q 520 120 540 140 Q 560 160 580 180 Q 600 200 620 220 Q 640 240 660 260" stroke="#0066cc" stroke-width="2.5" fill="none"/>
  <!-- Waypoints -->
  <circle cx="500" cy="100" r="3" fill="#ff6b6b"/>
  <circle cx="660" cy="260" r="3" fill="#00cc00"/>
  <!-- Annotations -->
  <text x="150" y="470" text-anchor="middle" class="label">Sharp corners</text>
  <text x="150" y="490" text-anchor="middle" class="label">Many waypoints</text>
  <text x="550" y="470" text-anchor="middle" class="label">Smooth trajectory</text>
  <text x="550" y="490" text-anchor="middle" class="label">Fewer waypoints</text>
</svg>'''

# Save SVG files
save_svg('figure_2_1_system_overview.svg', svg_fig_2_1)
save_svg('figure_2_2_path_planning.svg', svg_fig_2_2)
save_svg('figure_2_3_environment_modeling.svg', svg_fig_2_3)
save_svg('figure_2_4_path_smoothing.svg', svg_fig_2_4)

print("SVG files created successfully")

# Convert SVG to PNG
svg_to_png(svg_fig_2_1, figures_dir / 'figure_2_1_system_overview.png', 800, 600)
svg_to_png(svg_fig_2_2, figures_dir / 'figure_2_2_path_planning.png', 800, 600)
svg_to_png(svg_fig_2_3, figures_dir / 'figure_2_3_environment_modeling.png', 800, 600)
svg_to_png(svg_fig_2_4, figures_dir / 'figure_2_4_path_smoothing.png', 800, 600)

print("PNG files created successfully")

# Print mapping for reference
print("\nFigure Mapping:")
print("Figure 2.1: System overview of UGV")
print("Figure 2.2: Path Planning (2D vs 2.5D)")
print("Figure 2.3: 3D Environment Modeling Results")
print("Figure 2.4: Path Smoothing (Grid vs B-Spline)")
