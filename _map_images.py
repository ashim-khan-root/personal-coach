"""Map extracted images to rate card products and update rates.json"""
import json
from pathlib import Path

RATES_PATH = Path("coach/memory/rates.json")
QUOTE_RATES_PATH = Path("quotation-coach/coach/memory/rates.json")
IMG_DIR = Path("coach/memory/images")

# Map rate card keys to image files based on row descriptions
image_map = {
    # cameras
    "2mp_varifocal": {"col1": "row08-col1.png", "col3": "row08-col3.jpeg"},
    "2mp_eyeball": {"col1": "row09-col1.png", "col3": "row09-col3.png"},
    "2mp_bullet": {"col1": "row10-col1.png", "col3": "row10-col3.jpeg"},
    "4mp_kpoi": {"col1": "row17-col1.png", "col3": "row17-col3.png"},
    "4mp_anpr": {"col1": "row22-col1.png", "col3": "row22-col3.png"},
    "4mp_bullet": {"col1": "row10-col1.png", "col3": "row10-col3.jpeg"},
    "8mp_bullet": {"col1": "row10-col1.png", "col3": "row10-col3.jpeg"},
    "thermal": {},
    # nvrs
    "64ch_2mp": {"col1": "row06-col1.png", "col3": "row06-col3.jpeg"},
    "32ch_2mp": {"col1": "row06-col1.png", "col3": "row06-col3.jpeg"},
    "16ch_2mp": {"col1": "row06-col1.png", "col3": "row06-col3.jpeg"},
    "16ch_kpoi": {"col1": "row19-col1.png", "col3": "row19-col3.jpeg"},
    "16ch_anpr": {"col1": "row23-col1.png", "col3": "row23-col3.jpeg"},
    # hdd
    "4tb": {"col1": "row24-col1.jpeg", "col3": "row24-col3.jpeg"},
    "8tb": {"col1": "row20-col1.jpeg", "col3": "row20-col3.jpeg"},
    "16tb": {"col1": "row07-col1.jpeg", "col3": "row07-col3.jpeg"},
    # switches
    "8port_poe": {"col1": "row11-col1.png", "col3": "row11-col3.jpeg"},
    "16port_poe": {"col1": "row11-col1.png", "col3": "row11-col3.jpeg"},
    "24port_poe": {"col1": "row11-col1.png", "col3": "row11-col3.jpeg"},
    # racks
    "9u_wall": {},
    "18u": {"col1": "row13-col1.png", "col3": "row13-col3.png"},
    "27u": {"col1": "row12-col1.png", "col3": "row12-col3.png"},
    "42u": {"col1": "row12-col1.png", "col3": "row12-col3.png"},
    # monitors
    "24inch": {"col1": "row14-col1.png", "col3": "row14-col3.jpeg"},
    "32inch": {"col1": "row15-col1.png", "col3": "row15-col3.jpeg"},
    "43inch": {},
    # workstation
    "dell_optiplex": {"col1": "row16-col1.png", "col3": "row16-col3.jpeg"},
    "dell_precision": {},
    # ups
    "1kva_rack": {"col1": "row31-col1.jpeg", "col3": "row31-col3.jpeg"},
    "2kva_rack": {"col1": "row29-col1.jpeg", "col3": "row29-col3.jpeg"},
    "3kva_rack": {"col1": "row29-col1.jpeg", "col3": "row29-col3.jpeg"},
    # accessories
    "wall_mount": {},
    "bullet_base_box": {},
    "hanging_stand": {"col1": "row21-col3.jpeg", "col3": "row21-col3.jpeg"},
    "pole_mount": {},
    "pole_1_5m": {},
    "pole_3m": {},
    "patch_cord": {},
    "pdu": {},
    "patch_panel": {},
    "cable_manager": {},
    "cat6_cable_305m": {},
    "conduit_20mm": {},
    # licenses
    "hikcentral_base": {"col1": "row27-col1.png", "col3": "row27-col1.png"},
    "hikcentral_anpr_1ch": {"col1": "row28-col1.png", "col3": "row28-col1.png"},
    "hikcentral_extra_16ch": {},
    "vms_standard": {},
    # services
    "installation_per_camera": {"col1": "row41-col1.jpeg", "col3": "row41-col3.jpeg"},
    "installation_per_camera_high": {},
    "nvr_configuration": {},
    "dsa_dia_approvals": {},
    "dsa_dia_small": {},
    "amc_annual": {},
    "access_control": {},
    "access_control_plus": {},
}

# Header/logo image
logo_img = "row01-col1.jpeg"

def add_images_to_rates(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        rates = json.load(f)
    
    rates["_images"] = {
        "logo": logo_img,
        "base_path": "coach/memory/images/",
        "note": "Images extracted from demo-template.xlsx. Col1 = icon, Col3 = product photo."
    }
    
    count = 0
    for category, items in rates.items():
        if category.startswith("_"):
            continue
        for key in items:
            if key in image_map and image_map[key]:
                if "images" not in rates[category][key]:
                    rates[category][key]["images"] = {}
                for col, img in image_map[key].items():
                    if IMG_DIR.joinpath(img).exists():
                        rates[category][key]["images"][col] = img
                        count += 1
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rates, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {filepath}: {count} image references added")

add_images_to_rates(RATES_PATH)
add_images_to_rates(QUOTE_RATES_PATH)
print(f"\nLogo: {logo_img}")
print(f"Images dir: {IMG_DIR}")
