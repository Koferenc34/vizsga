from PIL import Image, ImageDraw, ImageFont
import os

def convert(file_path,text,userName, fileName):
    alreadyExist = False

    # Kép megnyitása
    image = Image.open(file_path)

    # Objekt létrehozása a vízjelnek
    watermark = Image.new('RGBA', image.size, (255, 255, 255, 0))

    # Vízjel interfész rajzolása és betűtípus beállítás
    draw = ImageDraw.Draw(watermark, 'RGBA')
    font = ImageFont.truetype('arial.ttf', 40)

    # pozíció és méret megadása és hozzáadása textbbox segítségével
    textbbox = draw.textbbox((0, 0), text, font=font)
    textwidth = textbbox[2] - textbbox[0]
    textheight = textbbox[3] - textbbox[1]
    width, height = image.size
    x = width - textwidth - 10
    y = height - textheight - 10

    draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))

    # Vízjel összefűzése az eredeti képpel
    watermarked = Image.alpha_composite(image.convert('RGBA'), watermark)

    # Kimeneti mappa és fájlnév létrehozása
    out_folder = r"output"
    file_name = f"WaterMarked_{text}_" + fileName
    
    # Kimeneti fájl útvonalának összeállítása
    out_path = os.path.join(out_folder, userName, file_name)

    if(os.path.exists(out_path)): alreadyExist = True

    # Mentés
    watermarked.save(out_path)

    return file_name, alreadyExist

