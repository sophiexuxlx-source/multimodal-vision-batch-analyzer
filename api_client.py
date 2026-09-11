import os
from dotenv import load_dotenv
from PIL import Image
from google import genai
import image_utils

# Load environment variables from .env file
load_dotenv()

def get_gemini_client() -> genai.Client:
    """Initializes and returns the Google GenAI client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is not set! Please create a .env file and set your free API key from https://aistudio.google.com/"
        )
    return genai.Client(api_key=api_key)

import time

def analyze_image(
    image_input: str | Image.Image | list,
    prompt: str = "Describe the contents of this image in detail.",
    model_name: str = "gemini-3.6-flash",
    max_retries: int = 3
) -> str:
    """
    Sends an image (file path, PIL Image, or list of PIL keyframes) along with a text prompt to Gemini Vision API.
    Handles temporary 503 high-demand or rate-limit errors with automatic model fallbacks.
    """
    client = get_gemini_client()

    # Prepare contents payload
    if isinstance(image_input, list):
        # List of PIL Images (e.g. keyframes)
        contents = image_input + [prompt]
    elif isinstance(image_input, str):
        if not os.path.exists(image_input):
            raise FileNotFoundError(f"Image path does not exist: {image_input}")
        img = Image.open(image_input)
        contents = [img, prompt]
    else:
        contents = [image_input, prompt]

    fallback_models = [model_name, "gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.1-flash-lite"]
    # Unique order
    models_to_try = list(dict.fromkeys(fallback_models))

    for target_model in models_to_try:
        for attempt in range(1, max_retries + 1):
            try:
                print(f"Sending request to {target_model} (Attempt {attempt}/{max_retries})...")
                response = client.models.generate_content(
                    model=target_model,
                    contents=contents
                )
                return response.text
            except Exception as e:
                err_msg = str(e)
                if ("503" in err_msg or "UNAVAILABLE" in err_msg or "429" in err_msg):
                    wait_time = attempt * 2
                    print(f"Model {target_model} busy (503/429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e
    raise RuntimeError("All Gemini vision models are currently experiencing high demand. Please retry in a few moments.")

if __name__ == "__main__":
    # Test script setup
    sample_path = "sample_image.png"
    if not os.path.exists(sample_path):
        image_utils.create_sample_image(sample_path)
    
    print("\n--- Testing Phase 1: Core API & Image Handling ---")
    try:
        result = analyze_image(
            image_input=sample_path,
            prompt="Identify all geometric shapes, colors, and text in this image."
        )
        print("\nAPI Response:")
        print(result)
    except Exception as e:
        print(f"\nExecution notice: {e}")
