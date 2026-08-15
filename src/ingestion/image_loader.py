import pytesseract   #This gives Python access to Tesseract OCR.
from PIL import Image, ImageOps, ImageEnhance   #Pillow allows us to load the medical report image.


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess an image before OCR.

    Steps:
        1. Convert image to grayscale.
        2. Increase contrast.

    Args:
        image: PIL Image object.

    Returns:
        Preprocessed PIL Image.
    """

    # Convert to grayscale
    grayscale = ImageOps.grayscale(image)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(grayscale)
    enhanced = enhancer.enhance(2.0)

    return enhanced


def extract_text_from_image(image_path: str) -> str:        #image_path: str - mean we're expecting a string path.
    #-> str - means the function returns text.
    """
    Extract text from a medical report image using Tesseract OCR.

    Parameters:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted text.
    """

    image = Image.open(image_path)

    processed_image = preprocess_image(image)

    text = pytesseract.image_to_string(image)

    return text.strip()