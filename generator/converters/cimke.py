from PIL import Image
import io
import fitz
from datetime import datetime
import os
from tqdm import tqdm


def convert(filePath, cols, rows, userName):
    images = pdf_to_images(filePath)   # Képek betöltése a PDF-ből
    pages = merge(images, cols, rows)  # Képek összefűzése oldalakra
    return export(pages, userName, cols, rows)     # Oldalak exportálása PDF-be

def pdf_to_images(pdf):
    # PDF fájl megnyitása
    pdf_document = fitz.open(pdf)
    images = []
    
    for page_number in tqdm(range(len(pdf_document)-1), "Címkék betöltése"):
        # Oldal betöltése
        page = pdf_document.load_page(page_number)
        
        # Az oldal képpé alakítása
        pix = page.get_pixmap()
        
        # Pixmap konvertálása bájtokba
        img_bytes = pix.tobytes()
        
        # Pillow kép létrehozása a bájtokból
        img = Image.open(io.BytesIO(img_bytes))
        
        # Kép hozzáadása a listához
        images.append(img)
    
    return images

def merge(images, cols, rows):
    pages = []
    pointer = 0
    left = 0
    top = 0
    right = 270
    bottom = 150
    for page in tqdm(range(10), "Oldalak létrehozása"):
        # Új oldal létrehozása fehér háttérrel
        back = Image.new('RGBA', (1070, 756),(255, 255, 255))
        y = 0
        for j in range(cols):
            x = 0
            for i in range(rows):
                # Kép kivágása és beillesztése az oldalra
                cropped = images[pointer].crop((left, top, right, bottom))
                back.paste(cropped, (x, y))
                x += right
                pointer += 1
            y += bottom
        pages.append(back)
    
    # Képek átalakítása RGB formátumra
    pages = [img.convert('RGB') for img in pages]
    return pages

def export(pages, username, cols, rows):
    alreadyExist = False
    # Kimeneti mappa és fájlnév létrehozása
    out_folder = r"output"
    file_name = "cimke-" + datetime.today().strftime("%Y-%m-%d") + f"_({rows}x{cols})" + ".pdf"
    
    # Kimeneti fájl útvonalának összeállítása
    out_path = os.path.join(out_folder, username, file_name)

    if(os.path.exists(out_path)): alreadyExist = True
    
    # Oldalak mentése PDF fájlba
    pages[0].save(out_path, save_all=True, append_images=pages[1:])

    return file_name, alreadyExist


