from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

figures_dir = Path('figures')
WIDTH, HEIGHT = 800, 600

class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 102, 204)
    LIGHT_BLUE = (232, 244, 248)
    GREEN = (0, 204, 0)
    RED = (255, 107, 107)
    GRAY = (150, 150, 150)
    LIGHT_GRAY = (240, 240, 240)

def create_figure_2_1():
    """System Overview of UGV"""
    img = Image.new('RGB', (WIDTH, HEIGHT), Color.WHITE)
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((20, 20), "System Overview of Unmanned Ground Vehicle (UGV)", fill=Color.BLACK)
    
    # Sensing Layer boxes
    for x, label in [(100, "LiDAR"), (320, "Camera"), (540, "IMU/GNSS")]:
        draw.rectangle([x-50, 80, x+50, 130], outline=Color.BLUE, fill=Color.LIGHT_BLUE, width=2)
        draw.text((x-40, 100), label[:8], fill=Color.BLUE)
    
    # Processing Layer
    draw.rectangle([100, 180, 700, 240], outline=Color.BLUE, fill=Color.LIGHT_BLUE, width=2)
    draw.text((200, 200), "Path Planning & Navigation", fill=Color.BLUE)
    
    # Output Layer
    for x, label in [(100, "Motor"), (320, "Vehicle"), (540, "Trajectory")]:
        draw.rectangle([x-50, 300, x+50, 350], outline=Color.GREEN, fill=(200, 220, 200), width=2)
        draw.text((x-40, 320), label, fill=Color.BLACK)
    
    # Arrows
    for x in [100, 320, 540]:
        draw.line([(x, 130), (x, 180)], fill=Color.BLUE, width=2)
        draw.polygon([(x-5, 175), (x+5, 175), (x, 180)], fill=Color.BLUE)
    
    for x in [100, 320, 540]:
        draw.line([(x, 240), (x, 300)], fill=Color.BLUE, width=2)
        draw.polygon([(x-5, 295), (x+5, 295), (x, 300)], fill=Color.BLUE)
    
    return img

def create_figure_2_2():
    """Path Planning 2D vs 2.5D"""
    img = Image.new('RGB', (WIDTH, HEIGHT), Color.WHITE)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 20), "Path Planning: 2D vs 2.5D Elevation Grid", fill=Color.BLACK)
    
    # 2D Path
    draw.text((100, 60), "2D Path", fill=Color.BLACK)
    draw.rectangle([60, 90, 280, 280], outline=Color.BLUE, fill=Color.LIGHT_BLUE, width=2)
    draw.line([(80, 130), (100, 150), (150, 160), (200, 200), (260, 250)], fill=Color.RED, width=3)
    draw.ellipse([(75, 125), (85, 135)], fill=Color.RED)
    draw.ellipse([(255, 245), (265, 255)], fill=Color.GREEN)
    draw.text((100, 300), "Simple Euclidean", fill=Color.BLACK)
    
    # 2.5D Path
    draw.text((520, 60), "2.5D Path", fill=Color.BLACK)
    draw.rectangle([460, 90, 680, 280], outline=Color.BLUE, fill=(232, 255, 232), width=2)
    draw.line([(480, 130), (500, 150), (530, 165), (570, 190), (610, 230), (660, 255)], 
              fill=Color.BLUE, width=3)
    draw.ellipse([(475, 125), (485, 135)], fill=Color.RED)
    draw.ellipse([(655, 250), (665, 260)], fill=Color.GREEN)
    
    # Elevation lines
    for y in [260, 230, 200]:
        draw.line([(460, y), (680, y)], fill=Color.GRAY, width=1)
    
    draw.text((500, 300), "Slope-Aware", fill=Color.BLACK)
    
    return img

def create_figure_2_3():
    """3D Environment Modeling"""
    img = Image.new('RGB', (WIDTH, HEIGHT), Color.WHITE)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 20), "3D Environment Modeling Results", fill=Color.BLACK)
    
    # Point Cloud
    draw.text((120, 60), "Point Cloud", fill=Color.BLACK)
    draw.rectangle([60, 90, 280, 280], outline=Color.BLUE, fill=Color.LIGHT_BLUE, width=2)
    
    points = [(100,130), (110,145), (130,150), (95,170), (115,180), (135,175), 
              (150,140), (160,165), (180,180), (200,150), (215,170)]
    for p in points:
        draw.ellipse([p[0]-2, p[1]-2, p[0]+2, p[1]+2], fill=Color.RED)
    
    draw.text((110, 300), "Sparse 3D Data", fill=Color.BLACK)
    
    # Elevation Grid
    draw.text((530, 60), "Elevation Grid", fill=Color.BLACK)
    draw.rectangle([460, 90, 680, 280], outline=Color.BLUE, fill=(232, 255, 232), width=2)
    
    # Grid cells
    colors = [(144, 238, 144), (124, 205, 124), (107, 184, 107), (128, 128, 128)]
    grid = [
        [(144,238,144), (144,238,144), (124,205,124), (105,105,105)],
        [(144,238,144), (144,238,144), (124,205,124), (105,105,105)],
        [(144,238,144), (124,205,124), (124,205,124), (169,169,169)],
    ]
    
    cell_w, cell_h = 40, 50
    for row, color_row in enumerate(grid):
        for col, color in enumerate(color_row):
            x1 = 470 + col * cell_w
            y1 = 100 + row * cell_h
            draw.rectangle([x1, y1, x1+cell_w-2, y1+cell_h-2], fill=color)
    
    draw.text((500, 300), "Color = Height", fill=Color.BLACK)
    
    return img

def create_figure_2_4():
    """Path Smoothing"""
    img = Image.new('RGB', (WIDTH, HEIGHT), Color.WHITE)
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 20), "Path Smoothing: Grid-Based vs B-Spline", fill=Color.BLACK)
    
    # Discrete
    draw.text((100, 60), "Discrete Path", fill=Color.BLACK)
    draw.rectangle([60, 100, 280, 280], outline=Color.LIGHT_GRAY, fill=Color.LIGHT_GRAY, width=1)
    
    # Grid
    for i in range(0, 230, 40):
        draw.line([(60, 100+i), (280, 100+i)], fill=(200, 200, 200))
        draw.line([(60+i, 100), (60+i, 280)], fill=(200, 200, 200))
    
    draw.line([(70, 120), (90, 140), (110, 160), (130, 180), (150, 200), 
               (170, 220), (190, 240), (210, 260)], fill=Color.RED, width=2)
    draw.ellipse([(65, 115), (75, 125)], fill=Color.RED)
    draw.ellipse([(205, 255), (215, 265)], fill=Color.GREEN)
    draw.text((80, 300), "Angular", fill=Color.BLACK)
    
    # Smooth
    draw.text((520, 60), "Smooth Path", fill=Color.BLACK)
    draw.rectangle([460, 100, 680, 280], outline=Color.LIGHT_GRAY, fill=Color.LIGHT_GRAY, width=1)
    
    for i in range(0, 230, 40):
        draw.line([(460, 100+i), (680, 100+i)], fill=(200, 200, 200))
        draw.line([(460+i, 100), (460+i, 280)], fill=(200, 200, 200))
    
    curve = [(470, 120), (485, 135), (500, 150), (520, 165), (540, 180), 
             (560, 200), (580, 220), (600, 240), (620, 260)]
    for i in range(len(curve)-1):
        draw.line([curve[i], curve[i+1]], fill=Color.BLUE, width=2)
    
    draw.ellipse([(465, 115), (475, 125)], fill=Color.RED)
    draw.ellipse([(615, 255), (625, 265)], fill=Color.GREEN)
    draw.text((500, 300), "Smooth", fill=Color.BLACK)
    
    return img

# Create all figures
print("Generating PNG figures directly...\n")

figures = [
    ("figure_2_1_system_overview.png", create_figure_2_1),
    ("figure_2_2_path_planning.png", create_figure_2_2),
    ("figure_2_3_environment_modeling.png", create_figure_2_3),
    ("figure_2_4_path_smoothing.png", create_figure_2_4),
]

for filename, create_func in figures:
    try:
        img = create_func()
        img.save(figures_dir / filename, 'PNG')
        print(f"✓ {filename}")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n✅ PNG figures created successfully!")
