from pathlib import Path

from PIL import ImageEnhance

def ensure_dir_exists(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def sharpen_image(image, level):
    sharpener = ImageEnhance.Sharpness(image)
    enhanced = sharpener.enhance(level)

    return enhanced