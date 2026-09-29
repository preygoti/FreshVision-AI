from PIL import Image
import numpy as np
from collections import deque
import glob, os

def clean_and_square_image(img):
    img = img.convert('RGB')
    w, h = img.size
    arr = np.array(img).copy()
    
    q = deque()
    visited = np.zeros((h, w), dtype=bool)
    
    # Border dark pixels
    for y in range(h):
        for x in (0, w - 1):
            if np.all(arr[y, x] < 45) and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if np.all(arr[y, x] < 45) and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))
                
    while q:
        cy, cx = q.popleft()
        arr[cy, cx] = [255, 255, 255]
        for ny, nx in ((cy-1, cx), (cy+1, cx), (cy, cx-1), (cy, cx+1)):
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                if np.all(arr[ny, nx] < 45):
                    visited[ny, nx] = True
                    q.append((ny, nx))
                    
    cleaned_img = Image.fromarray(arr)
    
    # Bounding box of fruit to center nicely
    non_white = np.any(arr < 240, axis=2)
    rows = np.where(non_white.any(axis=1))[0]
    cols = np.where(non_white.any(axis=0))[0]
    
    if len(rows) > 0 and len(cols) > 0:
        rmin, rmax = rows[0], rows[-1]
        cmin, cmax = cols[0], cols[-1]
        
        # Add a pleasant 8% margin around fruit
        fruit_w = cmax - cmin
        fruit_h = rmax - rmin
        margin = int(max(fruit_w, fruit_h) * 0.08)
        
        cmin = max(0, cmin - margin)
        rmin = max(0, rmin - margin)
        cmax = min(w - 1, cmax + margin)
        rmax = min(h - 1, rmax + margin)
        
        cropped_fruit = cleaned_img.crop((cmin, rmin, cmax, rmax))
        cw, ch = cropped_fruit.size
        side = max(cw, ch)
        
        square_img = Image.new('RGB', (side, side), (255, 255, 255))
        square_img.paste(cropped_fruit, ((side - cw) // 2, (side - ch) // 2))
    else:
        max_dim = max(w, h)
        square_img = Image.new('RGB', (max_dim, max_dim), (255, 255, 255))
        square_img.paste(cleaned_img, ((max_dim - w) // 2, (max_dim - h) // 2))

    return square_img.resize((320, 320), Image.Resampling.LANCZOS)

def process_all():
    target_dirs = [
        os.path.join('static', 'samples'),
        os.path.join('public', 'static', 'samples')
    ]
    
    for filename in ['freshapples.jpg', 'rottenapples.jpg', 'freshbanana.jpg', 'rottenbanana.jpg', 'freshoranges.jpg', 'rottenoranges.jpg']:
        src_path = os.path.join('static', 'samples', filename)
        if not os.path.exists(src_path):
            continue
        im = Image.open(src_path)
        cleaned = clean_and_square_image(im)
        
        for d in target_dirs:
            os.makedirs(d, exist_ok=True)
            out_path = os.path.join(d, filename)
            cleaned.save(out_path, format='JPEG', quality=95)
            print(f'[+] Cleaned and saved: {out_path}')

if __name__ == '__main__':
    process_all()
