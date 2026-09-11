import os
import glob
import json
import csv
import random
from PIL import Image
import use_cases

DEFAULT_PHOTOS_DIR = r"c:\AI Builder & AI Architect\AI Study\AI Builders\Project 2 Downloading Imagines from an Instagram Account\photos"

def get_all_photos(photos_dir: str = DEFAULT_PHOTOS_DIR) -> list[str]:
    """Finds all image files in the specified directory."""
    if not os.path.exists(photos_dir):
        print(f"Warning: Photos directory does not exist: {photos_dir}")
        return []
    
    extensions = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
    image_files = set()
    for ext in extensions:
        image_files.update(glob.glob(os.path.join(photos_dir, ext)))
        # Also check uppercase extensions without duplicating
        image_files.update(glob.glob(os.path.join(photos_dir, ext.upper())))
    return sorted(list(image_files))

def analyze_photo_batch(
    photos_dir: str = DEFAULT_PHOTOS_DIR,
    sample_size: int = 5,
    output_json: str = "batch_analysis_results.json",
    output_csv: str = "batch_analysis_results.csv"
):
    """
    Analyzes a sample batch of photos from the downloaded dataset and saves results.
    """
    all_photos = get_all_photos(photos_dir)
    total_found = len(all_photos)
    print(f"Found {total_found} total photos in: {photos_dir}")

    if total_found == 0:
        print("No photos found to process.")
        return

    # Select sample
    selected = random.sample(all_photos, min(sample_size, total_found))
    print(f"Selected {len(selected)} photos for batch analysis...\n")

    results = []

    for i, photo_path in enumerate(selected, 1):
        filename = os.path.basename(photo_path)
        print(f"[{i}/{len(selected)}] Processing: {filename}...")
        
        try:
            desc = use_cases.generate_image_description(photo_path)
            alt_text = use_cases.generate_alt_text(photo_path)
            objects_json = use_cases.detect_objects(photo_path)

            record = {
                "file_name": filename,
                "file_path": photo_path,
                "description": desc,
                "alt_text": alt_text,
                "detected_objects": objects_json
            }
            results.append(record)
            print(f"  [OK] Description generated ({len(desc)} chars)")
            print(f"  [OK] Alt-text: '{alt_text}'")
        except Exception as e:
            print(f"  [ERROR] Error analyzing {filename}: {e}")

    # Save to JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved JSON results to: {output_json}")

    # Save to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Alt Text", "Description", "Detected Objects Summary"])
        for r in results:
            objs_summary = ", ".join([obj.get("name", "") for obj in r.get("detected_objects", {}).get("objects", [])])
            writer.writerow([r["file_name"], r["alt_text"], r["description"], objs_summary])
    print(f"Saved CSV results to: {output_csv}")

if __name__ == "__main__":
    analyze_photo_batch(sample_size=3)
