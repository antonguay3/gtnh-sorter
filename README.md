# GTNH Items Color Sorter and Searcher

A tool I made to sort items by color in minecraft gtnh.


## How to Use

Download and extract zip

### Get item icons from minecraft
1. In a minecraft world, open your inventory and NEI/JEI/REI overlay.
2. Toggle "Collapse/Expand All Collapsible Items" to expand all items.
3. Search for the item/s you want to extract or leave blank to extract all.
4. Open the NEI/JEI/REI config menu, go to Tools > Data Dumps.
5. Find Item Panels, click the button next to "Dump" until it says "PNG", then select texture size (default 16x16).
6. Click Dump, and wait for process to finish.
7. All PNG's will be saved at `AppData\Roaming\PrismLauncher\instances\GT_New_Horizons_2.8.4_Java_17-25\.minecraft\dumps\itempanel_icons` for prism launcher.
8. In vanilla minecraft it's at `AppData\Roaming\.minecraft\versions\GT_New_Horizons_2.8.4_Java_17-25\dumps\itempanel_icons`.

     - ("GT_New_Horizons_2.8.4_Java_17-25" is the name of your pack or version).


### 1. Generating a Color Sorted Guide
1. Go to the `sort_items/` folder and paste all the item PNG textures you want to sort.
2. Double-click **`Sort_items.bat`**.
3. *Optional:* On the first run, the script will ask you for your storage layout dimensions (e.g., type `32x8` or press **Enter** to use the default configuration).
4. The script will automatically install dependencies on its first launch, read the items, sort them  by color, and save a template map inside `output_images/color_grid_guide.png`.

### 2. Searching for an Item's Coordinates
1. Go to the `search_item/` folder and paste your item PNG textures.
2. Double-click **`Search_item.bat`**.
3. Type the **name of the item** or directly **drag and drop a PNG file (from the `search_item` folder)** into the terminal window.
4. The application will output the exact **[ Column ]** and **[ Row ]** where that item belongs in your grid layout.
    
    Type `config` at any time inside the search engine to change your grid dimensions.
