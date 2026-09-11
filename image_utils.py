import base64
import os
from PIL import Image, ImageDraw

def encode_image_to_base64(image_path: str) -> str:
    """Encodes a local image file to a base64 string."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def load_pil_image(image_path: str) -> Image.Image:
    """Loads an image file into a PIL Image object."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    return Image.open(image_path)

def create_sample_image(output_path: str = "sample_image.png") -> str:
    """Creates a sample test image with geometric shapes and text."""
    width, height = 400, 300
    img = Image.new("RGB", (width, height), color=(240, 244, 248))
    draw = ImageDraw.Draw(img)
    
    # Draw background accents
    draw.rectangle([20, 20, 380, 280], outline=(70, 130, 180), width=3)
    
    # Draw shapes (Red circle, Green rectangle, Yellow triangle)
    draw.ellipse([40, 50, 140, 150], fill=(235, 87, 87), outline=(180, 40, 40), width=2)
    draw.rectangle([170, 50, 270, 150], fill=(39, 174, 96), outline=(20, 120, 60), width=2)
    draw.polygon([(330, 50), (360, 130), (290, 130)], fill=(242, 201, 76), outline=(200, 160, 40))
    
    # Add text banner
    draw.rectangle([40, 190, 360, 250], fill=(44, 62, 80))
    draw.text((60, 210), "AI Builders - Project 4 Test Image", fill=(255, 255, 255))
    
    img.save(output_path)
    print(f"Sample image successfully created at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_sample_image()
