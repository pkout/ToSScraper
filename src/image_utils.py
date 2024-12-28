from PIL import ImageEnhance

def sharpen(image, level):
    sharpener = ImageEnhance.Sharpness(image)
    enhanced = sharpener.enhance(level)

    return enhanced