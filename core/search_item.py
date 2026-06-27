import os
import json
import colorsys
import numpy as np
from PIL import Image
from tqdm import tqdm

# --- CONFIGURATION PATHS ---
CONFIG_FILE = "./config.json"
INPUT_FOLDER = "../search_item"

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
            data = np.array(img)
            
            r = data[:, :, 0]
            g = data[:, :, 1]
            b = data[:, :, 2]
            a = data[:, :, 3]
            
            mask = a > 50
            if not np.any(mask):
                return (0, 0, 0)
                
            r_avg = np.mean(r[mask]) / 255.0
            g_avg = np.mean(g[mask]) / 255.0
            b_avg = np.mean(b[mask]) / 255.0
            
            return colorsys.rgb_to_hsv(r_avg, g_avg, b_avg)
    except:
        return (0, 0, 0)

def calculate_positions(grid_width, grid_height):
    item_data = []
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' not found.")
        return {}

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith('.png')]
    
    print("Analyzing item colors:")
    for filename in tqdm(files, desc="Loading database", unit="item"):
        path = os.path.join(INPUT_FOLDER, filename)
        h, s, v = get_average_hsv(path)
        item_data.append({'name': filename, 'path': path, 'h': h, 's': s, 'v': v})
    
    if not item_data:
        return {}

    item_data.sort(key=lambda x: x['h'])
    
    total_items = len(item_data)
    items_per_col = max(1, total_items // grid_width)
    
    positions = {}
    
    for col in range(grid_width):
        start_idx = col * items_per_col
        end_idx = (col + 1) * items_per_col if col < (grid_width - 1) else total_items
        
        col_items = item_data[start_idx:end_idx]
        col_items.sort(key=lambda x: x['v'], reverse=True)
        
        col_size = len(col_items)
        for index, item in enumerate(col_items):
            calculated_row = min(grid_height, (index // max(1, col_size // grid_height)) + 1)
            calculated_col = col + 1
            
            positions[item['name'].lower()] = (int(calculated_row), calculated_col)
    
    return positions

def main():
    config = load_config()
    grid_width = config["GRID_WIDTH"]
    grid_height = config["GRID_HEIGHT"]

    print(f"Grid setup loaded: {grid_width} columns x {grid_height} rows.")
    print("Type 'config' to update dimensions, or search directly.")
    
    positions = calculate_positions(grid_width, grid_height)
    print("\nReady")
    print("-" * 50)
    print("Instructions: Type the item name OR drag and drop the PNG file here.")
    print("Type 'config' to update grid, 'exit' to close application.")
    print("-" * 50)

    while True:
        user_input = input("\nEnter item, drag PNG or type command: ").strip()
        if user_input.lower() == 'exit':
            break
            
        if not user_input:
            continue

        # Configuration routing
        if user_input.lower() == 'config':
            print(f"\nCurrent setup: {grid_width}x{grid_height}")
            new_dims = input("Enter new dimensions (e.g., '32x8') or press Enter to cancel: ").strip().lower()
            if new_dims:
                try:
                    w_str, h_str = new_dims.split('x')
                    grid_width = int(w_str)
                    grid_height = int(h_str)
                    save_config(grid_width, grid_height)
                    print(f" Saved! Re-calculating database coordinates based on {grid_width}x{grid_height}...")
                    positions = calculate_positions(grid_width, grid_height)
                except:
                    print(" Invalid format! Keeping active setup.")
            continue

        user_input = user_input.strip('"').strip("'")

        if user_input.lower().endswith('.png'):
            filename_to_search = os.path.basename(user_input).lower()
        else:
            filename_to_search = user_input.lower()
            if not filename_to_search.endswith('.png'):
                filename_to_search += '.png'

        if filename_to_search in positions:
            coords = positions[filename_to_search]
            print(f"\n Exact match found -> {filename_to_search.upper()}")
            print(f" PLACE AT -> [ Column: {coords[1]} ] [ Row: {coords[0]} ]")
            continue

        matches = []
        for item_name, coords in positions.items():
            if filename_to_search.replace('.png', '') in item_name:
                matches.append((item_name, coords))
        
        if not matches:
            print("Item not found")
            continue

        if len(matches) == 1:
            item_name, coords = matches[0]
            print(f"\n Partial match found -> {item_name.upper()}")
            print(f" PLACE AT -> [ Column: {coords[1]} ] [ Row: {coords[0]} ]")
        else:
            print(f"\n🔍 Multiple items found ({len(matches)} matches). Please choose one:")
            display_limit = min(26, len(matches))
            
            for i in range(display_limit):
                print(f"  [{i + 1}] {matches[i][0].upper()}")
            
            if len(matches) > 26:
                print(f"  ... and {len(matches) - 26} more items.")

            try:
                choice = input(f"\nSelect number (1-{display_limit}) or press Enter to skip: ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < display_limit:
                        item_name, coords = matches[idx]
                        print(f"\n PLACE AT -> [ Column: {coords[1]} ]  [ Row: {coords[0]} ]")
                    else:
                        print(" Invalid selection.")
            except ValueError:
                print(" Invalid input.")

if __name__ == "__main__":
    main()