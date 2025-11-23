import os
import sys
from PIL import Image

def convert_images(source_folder, output_format="JPEG", target_width=None):
    # Create output folder
    output_folder = f"converted_{output_format.lower()}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"[+] Output folder created: {output_folder}")

    # Loop through files
    valid_exts = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
    count = 0

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(valid_exts):
            img_path = os.path.join(source_folder, filename)
            try:
                with Image.open(img_path) as img:
                    # 1. RESIZE LOGIC (The Value Add)
                    if target_width:
                        w_percent = (target_width / float(img.size[0]))
                        h_size = int((float(img.size[1]) * float(w_percent)))
                        img = img.resize((target_width, h_size), Image.Resampling.LANCZOS)

                    # 2. FIX TRANSPARENCY CRASH (The Safety Net)
                    if output_format.upper() in ["JPG", "JPEG"] and img.mode == 'RGBA':
                        img = img.convert('RGB')

                    # Define new filename
                    clean_name = os.path.splitext(filename)[0]
                    new_filename = f"{clean_name}.{output_format.lower()}"
                    save_path = os.path.join(output_folder, new_filename)

                    # Convert and Save with optimization
                    img.save(save_path, output_format, quality=85)
                    print(f"✅ Processed: {filename} -> {new_filename}")
                    count += 1
            except Exception as e:
                print(f"❌ Failed: {filename} - {e}")
    
    print(f"\nDone! Processed {count} images.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python image_fixer.py [folder_path]")
        print("Example: python image_fixer.py ./my_images")
    else:
        folder = sys.argv[1]
        # Hardcoding width to 1080px for 'Web Optimization' default
        convert_images(folder, target_width=1080)
