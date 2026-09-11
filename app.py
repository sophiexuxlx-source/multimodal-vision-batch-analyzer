import os
import json
import random
import image_utils
import api_client
import use_cases
import batch_analyzer

INSTAGRAM_PHOTOS_DIR = r"c:\AI Builder & AI Architect\AI Study\AI Builders\Project 2 Downloading Imagines from an Instagram Account\photos"

def main():
    print("=" * 65)
    print("  Multimodal AI Image Content Analysis App")
    print("  (Connected with Project 2 Instagram Dataset: 911 Photos)")
    print("=" * 65)
    
    # Load Instagram photos list
    ig_photos = batch_analyzer.get_all_photos(INSTAGRAM_PHOTOS_DIR)
    if ig_photos:
        print(f"[OK] Found {len(ig_photos)} photos in your Project 2 dataset!")
        current_image = random.choice(ig_photos)
    else:
        default_image = "sample_image.png"
        if not os.path.exists(default_image):
            image_utils.create_sample_image(default_image)
        current_image = default_image

    while True:
        print(f"\n[Current Active Image: {os.path.basename(current_image)}]")
        print(f" Full Path: {current_image}")
        print("\nSelect an option:")
        print("  1. Describe Image / Ask Question (Use Case 1)")
        print("  2. Generate Alt-Text for Web (Use Case 2)")
        print("  3. Detect Objects in JSON Format (Use Case 3)")
        print("  4. Pick a Random Photo from Instagram Dataset")
        print("  5. Pick Photo by Index (1 to 900+)")
        print("  6. Run Batch Analysis on N Photos (Export to CSV & JSON)")
        print("  7. Enter Custom Image Path")
        print("  8. Exit")

        choice = input("\nEnter choice (1-8): ").strip()

        if choice == "1":
            q = input("Enter a custom question (or press Enter for full description): ").strip()
            print("\nAnalyzing image with Gemini Vision API...")
            try:
                res = use_cases.generate_image_description(current_image, custom_question=q if q else None)
                print("\n--- Analysis Result ---")
                print(res)
            except Exception as e:
                print(f"\nError analyzing image: {e}")

        elif choice == "2":
            print("\nGenerating Alt-Text...")
            try:
                alt = use_cases.generate_alt_text(current_image)
                print("\n--- Generated Alt-Text ---")
                print(f'HTML Tag: <img src="{os.path.basename(current_image)}" alt="{alt}" />')
                print(f'Alt-Text: {alt}')
            except Exception as e:
                print(f"\nError generating alt-text: {e}")

        elif choice == "3":
            print("\nDetecting Objects...")
            try:
                objects_json = use_cases.detect_objects(current_image)
                print("\n--- Detected Objects (JSON) ---")
                print(json.dumps(objects_json, indent=2))
            except Exception as e:
                print(f"\nError detecting objects: {e}")

        elif choice == "4":
            if ig_photos:
                current_image = random.choice(ig_photos)
                print(f"Selected random Instagram photo: {os.path.basename(current_image)}")
            else:
                print("No Instagram photos directory found.")

        elif choice == "5":
            if ig_photos:
                user_inp = input(f"Enter photo index (1-{len(ig_photos)}) or filename: ").strip()
                # Check if user entered a valid index number within 1..len
                if user_inp.isdigit() and 1 <= int(user_inp) <= len(ig_photos):
                    idx = int(user_inp) - 1
                    current_image = ig_photos[idx]
                    print(f"[OK] Selected photo #{idx+1}: {os.path.basename(current_image)}")
                else:
                    # Search by filename
                    matches = [(i + 1, p) for i, p in enumerate(ig_photos) if user_inp.lower() in os.path.basename(p).lower()]
                    if matches:
                        idx, current_image = matches[0]
                        print(f"[OK] Found and selected photo #{idx}: {os.path.basename(current_image)}")
                    else:
                        print(f"No photo found matching: '{user_inp}'")
            else:
                print("No Instagram dataset found.")

        elif choice == "6":
            count_str = input("How many photos to analyze in batch? (e.g. 5): ").strip()
            try:
                count = int(count_str)
                batch_analyzer.analyze_photo_batch(INSTAGRAM_PHOTOS_DIR, sample_size=count)
            except ValueError:
                print("Invalid number.")

        elif choice == "7":
            new_path = input("Enter path to custom image file: ").strip().strip('"').strip("'")
            if os.path.exists(new_path):
                current_image = new_path
                print(f"Switched image to: {current_image}")
            else:
                print(f"File not found: {new_path}")

        elif choice == "8":
            print("Exiting Image Content Analysis App. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
