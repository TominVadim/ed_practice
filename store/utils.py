import os
from PIL import Image
from django.conf import settings

def resize_image(image_path, width=300, height=200):
    """Изменение размера изображения до 300x200"""
    try:
        img = Image.open(image_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img.save(image_path)
        return True
    except Exception as e:
        print(f'Error resizing image: {e}')
        return False

def delete_old_image(image_path):
    """Удаление старого изображения"""
    if image_path and os.path.isfile(image_path):
        os.remove(image_path)
        return True
    return False
