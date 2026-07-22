from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageDraw, ImageFont

pdf_path = Path('UMP Template.pdf')
if not pdf_path.exists():
    raise FileNotFoundError(pdf_path)

out_pdf = Path('UMP Template - with sketches.pdf')
fig_dir = Path('figures_from_ump')
fig_dir.mkdir(exist_ok=True)

mappings = []

doc = fitz.open(pdf_path)
for pno in range(len(doc)):
    page = doc[pno]
    images = page.get_images(full=True)
    if not images:
        continue
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        ext = base_image["ext"]
        img_name = f'ump_page{pno+1}_img{img_index+1}.{ext}'
        img_path = fig_dir / img_name
        with open(img_path, 'wb') as f:
            f.write(image_bytes)
        mappings.append({'page': pno, 'img_path': img_path})

# create sketch copies (simple border + label)
sketches = []
for m in mappings:
    p = m['img_path']
    im = Image.open(p).convert('RGB')
    # add white border
    border = 20
    im_with_border = ImageOps.expand(im, border=border, fill='white')
    # draw small label at bottom
    draw = ImageDraw.Draw(im_with_border)
    try:
        font = ImageFont.truetype('arial.ttf', 18)
    except Exception:
        font = ImageFont.load_default()
    text = 'Figure (sketch)'
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except Exception:
        tw, th = font.getsize(text)
    x = (im_with_border.width - tw) // 2
    y = im_with_border.height - th - 8
    draw.text((x, y), text, fill='black', font=font)
    sketch_name = p.stem + '_sketch.png'
    sketch_path = fig_dir / sketch_name
    im_with_border.save(sketch_path, format='PNG')
    sketches.append({'page': m['page'], 'sketch_path': sketch_path})

# insert sketch pages after original pages (keep order)
# open original again for modification
doc = fitz.open(pdf_path)
inserted = 0
for s in sketches:
    target_page = s['page'] + inserted
    # page dimensions
    ref_page = doc[target_page]
    rect = ref_page.rect
    # insert an empty page after target_page
    new_page = doc.new_page(pno=target_page+1, width=rect.width, height=rect.height)
    # fit image into page while keeping aspect ratio
    img = Image.open(s['sketch_path'])
    iw, ih = img.size
    # compute placement box
    pw = rect.width
    ph = rect.height
    # scale image to fit within page with margin
    margin = 72  # 1 inch
    max_w = pw - 2*margin
    max_h = ph - 2*margin
    scale = min(max_w/iw, max_h/ih, 1.0)
    draw_w = int(iw*scale)
    draw_h = int(ih*scale)
    x0 = (pw - draw_w)/2
    y0 = (ph - draw_h)/2
    img_rect = fitz.Rect(x0, y0, x0+draw_w, y0+draw_h)
    new_page.insert_image(img_rect, filename=str(s['sketch_path']))
    inserted += 1

# save modified pdf
if out_pdf.exists():
    out_pdf.unlink()

doc.save(out_pdf)
print('Saved', out_pdf)
