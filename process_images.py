import os
from PIL import Image

brain_dir = r"C:\Users\Jahnavi\.gemini\antigravity-ide\brain\fc1419f3-82ac-43f0-bad4-c814c25ed8a4"
assets_dir = r"c:\Users\Jahnavi\OneDrive\Desktop\concierge\conciergeiq\src\assets"
images_dir = r"c:\Users\Jahnavi\OneDrive\Desktop\concierge\conciergeiq\src\assets\images"

img1_path = os.path.join(brain_dir, "media__1784361895092.png")
img2_path = os.path.join(brain_dir, "media__1784361901524.png")

# Accent Colors
GOLD_COLOR = (255, 213, 79)  # #FFD54F
CYAN_COLOR = (102, 217, 255) # #66d9ff
WHITE_COLOR = (255, 255, 255) # #ffffff
DARK_BLUE = (8, 27, 61)

def make_transparent_and_color(img_path, output_path, target_color=(255, 255, 255), is_img1=False):
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        r, g, b, a = item
        is_bg = False
        if is_img1:
            if r > 210 and g > 210 and b > 200:
                is_bg = True
        else:
            if r > 240 and g > 240 and b > 240:
                is_bg = True
                
        if is_bg:
            new_data.append((0, 0, 0, 0)) # Transparent
        else:
            new_data.append((*target_color, 255))
            
    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Saved transparent version to {output_path}")

# Load cropped icons generated in the previous run
palm_tree_raw = os.path.join(brain_dir, "palm_tree_raw.png")
person_raw = os.path.join(brain_dir, "person_raw.png")

# Generate colored versions of Palm Tree Logo
make_transparent_and_color(palm_tree_raw, os.path.join(assets_dir, "logo_palm_white.png"), target_color=WHITE_COLOR, is_img1=True)
make_transparent_and_color(palm_tree_raw, os.path.join(assets_dir, "logo_palm_gold.png"), target_color=GOLD_COLOR, is_img1=True)
make_transparent_and_color(palm_tree_raw, os.path.join(assets_dir, "logo_palm_cyan.png"), target_color=CYAN_COLOR, is_img1=True)

# Generate colored versions of Suitcase Person Logo
make_transparent_and_color(person_raw, os.path.join(assets_dir, "logo_person_white.png"), target_color=WHITE_COLOR, is_img1=False)
make_transparent_and_color(person_raw, os.path.join(assets_dir, "logo_person_gold.png"), target_color=GOLD_COLOR, is_img1=False)
make_transparent_and_color(person_raw, os.path.join(assets_dir, "logo_person_cyan.png"), target_color=CYAN_COLOR, is_img1=False)

# Generate Favicons in different colors
for name, color in [("gold", GOLD_COLOR), ("cyan", CYAN_COLOR), ("white", WHITE_COLOR)]:
    fav_path_png = os.path.join(assets_dir, f"favicon_{name}.png")
    make_transparent_and_color(palm_tree_raw, fav_path_png, target_color=color, is_img1=True)
    
    # Save as ICO
    fav_png = Image.open(fav_path_png)
    fav_png.thumbnail((64, 64))
    fav_png.save(os.path.join(assets_dir, f"favicon_{name}.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

# Copy default Gold favicon to standard locations
import shutil
shutil.copy(os.path.join(assets_dir, "favicon_gold.png"), os.path.join(assets_dir, "favicon.png"))
shutil.copy(os.path.join(assets_dir, "favicon_gold.png"), os.path.join(images_dir, "favicon.png"))
shutil.copy(os.path.join(assets_dir, "favicon_gold.ico"), os.path.join(assets_dir, "favicon.ico"))
shutil.copy(os.path.join(assets_dir, "favicon_gold.ico"), r"c:\Users\Jahnavi\OneDrive\Desktop\concierge\conciergeiq\src\favicon.ico")

print("All colored image assets generated successfully!")
