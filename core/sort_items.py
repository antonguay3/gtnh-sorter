import os
import json
import colorsys
import numpy as np
from PIL import Image

# --- CONFIGURATION PATHS ---
CONFIG_FILE = "./config.json"
INPUT_FOLDER = "../sort_items"
OUTPUT_IMAGE = "../output_images/color_grid_guide.png"
THUMB_SIZE = 32  # Size of each item slot in the final guide image

def load_config():
    defaults = {"GRID_WIDTH": 32, "GRID_HEIGHT": 8}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return defaults

def save_config(width, height):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"GRID_WIDTH": width, "GRID_HEIGHT": height}, f, indent=4)

def get_average_hsv(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            
            # Using NumPy avoids the DeprecationWarning and fixes the type comparison error
            data = np.array(img)
            
            r = data[:, :, 0]
            g = data[:, :, 1]
            b = data[:, :, 2]
            a = data[:, :, 3]
            
            # Create a mask for non-transparent pixels
            mask = a > 50
            if not np.any(mask):
                return (0, 0, 0)  # Transparent fallback
                
            # Calculate averages safely
            r_avg = np.mean(r[mask]) / 255.0
            g_avg = np.mean(g[mask]) / 255.0
            b_avg = np.mean(b[mask]) / 255.0
            
            return colorsys.rgb_to_hsv(r_avg, g_avg, b_avg)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return (0, 0, 0)

def main():
    # Setup grid configuration
    config = load_config()
    current_w = config["GRID_WIDTH"]
    current_h = config["GRID_HEIGHT"]

    print(f"Current grid setup: {current_w} columns x {current_h} rows.")
    user_input = input("Enter new dimensions (e.g., '32x8') or press Enter to skip: ").strip().lower()
    
    if user_input:
        try:
            w_str, h_str = user_input.split('x')
            GRID_WIDTH = int(w_str)
            GRID_HEIGHT = int(h_str)
            save_config(GRID_WIDTH, GRID_HEIGHT)
            print(f" Saved grid settings: {GRID_WIDTH}x{GRID_HEIGHT}\n")
        except:
            print("Invalid format! Continuing with previous dimensions.\n")
            GRID_WIDTH = current_w
            GRID_HEIGHT = current_h
    else:
        GRID_WIDTH = current_w
        GRID_HEIGHT = current_h

    # Get images and analyze
    item_data = []
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' not found. Please create it and add your PNGs.")
        return

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith('.png'):
            path = os.path.join(INPUT_FOLDER, filename)
            h, s, v = get_average_hsv(path)
            item_data.append({'path': path, 'h': h, 's': s, 'v': v})
    
    total_slots = GRID_WIDTH * GRID_HEIGHT
    print(f"Found {len(item_data)} items. Target grid slots available: {total_slots}")
    
    if len(item_data) == 0:
        print("No PNG images found in the items folder!")
        return

    while len(item_data) < total_slots:
        item_data.append({'path': None, 'h': 0, 's': 0, 'v': 0})
    
    if len(item_data) > total_slots:
        print(f"Warning: Too many items ({len(item_data)}). Trimming to {total_slots} items.")
        item_data = item_data[:total_slots]

    item_data.sort(key=lambda x: x['h'])
    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    for col in range(GRID_WIDTH):
        col_items = item_data[col * GRID_HEIGHT : (col + 1) * GRID_HEIGHT]
        col_items.sort(key=lambda x: x['v'], reverse=True)
        for row in range(GRID_HEIGHT):
            grid[row][col] = col_items[row]

    guide_img = Image.new("RGBA", (GRID_WIDTH * THUMB_SIZE, GRID_HEIGHT * THUMB_SIZE), (30, 30, 30, 255))
    
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            cell = grid[row][col]
            if cell and cell['path']:
                try:
                    with Image.open(cell['path']) as icon:
                        icon = icon.resize((THUMB_SIZE, THUMB_SIZE), Image.Resampling.NEAREST)
                        guide_img.paste(icon, (col * THUMB_SIZE, row * THUMB_SIZE), icon.convert("RGBA"))
                except:
                    pass
                
    os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)
    guide_img.save(OUTPUT_IMAGE)
    print(f"Done! Output saved to: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()