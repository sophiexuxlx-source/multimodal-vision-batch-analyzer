import json
from PIL import Image
from google import genai
import api_client

def generate_image_description(image_input: str | Image.Image | list, custom_question: str = None) -> str:
    """
    Use Case 1: General Image Description & Q&A.
    Describes the image or answers a user question about its content.
    """
    if custom_question:
        prompt = f"Answer the following question about this image/sequence in detail: {custom_question}"
    else:
        prompt = (
            "Analyze this image/sequence and provide a clear, comprehensive description of its visual contents, "
            "including key objects, colors, text, composition, movement/progression over time, and context."
        )
    return api_client.analyze_image(image_input=image_input, prompt=prompt)

def generate_alt_text(image_input: str | Image.Image | list) -> str:
    """
    Use Case 2: Alt-Text Generation for Web Accessibility.
    Generates a concise, WCAG-compliant image description under 125 characters.
    """
    prompt = (
        "Generate a concise, accessible alt-text description for this image for HTML web pages. "
        "Rules:\n"
        "1. Keep it under 125 characters.\n"
        "2. Do NOT start with 'Image of...' or 'Picture showing...'.\n"
        "3. Focus on essential subject matter and context.\n"
        "Output ONLY the alt-text string, with no additional text or quotes."
    )
    return api_client.analyze_image(image_input=image_input, prompt=prompt).strip()

def detect_objects(image_input: str | Image.Image | list) -> dict:
    """
    Use Case 3: Object Recognition & Structured Output (JSON).
    Identifies objects in the image and returns a structured JSON breakdown.
    """
    prompt = (
        "Analyze this image and identify all major visible objects.\n"
        "Return your response ONLY as a raw JSON object with the following schema:\n"
        "{\n"
        '  "total_objects_count": int,\n'
        '  "objects": [\n'
        '    {"name": "object_name", "category": "category_name", "color": "color_name", "location": "description"}\n'
        '  ]\n'
        "}\n"
        "Do not include markdown code block formatting (like ```json). Return pure JSON text."
    )
    
    raw_response = api_client.analyze_image(image_input=image_input, prompt=prompt)
    
    # Clean response in case model included markdown quotes
    cleaned = raw_response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"raw_output": raw_response, "error": "Could not parse JSON output"}

if __name__ == "__main__":
    print("Use Cases Module loaded. Ready to run against configured Gemini Vision client.")
