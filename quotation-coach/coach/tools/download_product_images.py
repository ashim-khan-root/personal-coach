import requests
import os
import re
from pathlib import Path

IMG_DIR = Path(__file__).resolve().parent.parent / "memory" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTS = {
    # cameras
    "2mp-fixed-hikvision-bullet-camera.png": [
        "https://assets.hikvision.com/prd/normal/all/image/m000041483/筒机45-基线-4K-主图.png.thumb.1280.1280.png",
        "https://www.hikvision.com/content/dam/hikvision/en/products/S000000001/S000000132/S000000146/S000000147/OFR000203/M000001020/Product_Image/DS-2CE16H0T-ITFS_3.6mm_RightAngle45.png.thumb.1280.1280.png",
    ],
    "2mp-lite-ir-fixed-focal-eyeball-network-camera.png": [
        "https://assets.hikvision.com/prd/public/all/image/m000057227/DS-2CD2386G2-IU_20211101_1.png.thumb.1280.1280.png",
        "https://www.hikvision.com/content/dam/hikvision/en/products/S000000001/S000000132/S000000146/S000000148/OFR000204/M000001027/Product_Image/DS-2CE76D0T-ITMF_3.6mm_RightAngle45.png.thumb.1280.1280.png",
    ],
    "2mp-acusense-motorized-varifocal-network-camera.jpeg": [
        "https://assets.hikvision.com/prd/public/all/image/m000019593/右45°图.png.thumb.1280.1280.png",
    ],
    "hikvision-4mp-kpoi-camera.png": [
        "https://assets.hikvision.com/prd/public/all/image/m000019593/右45°图.png.thumb.1280.1280.png",
        "https://www.hikvision.com/content/dam/hikvision/en/products/S000000001/S000000002/S000000003/S000000006/OFR000005/M000019593/Product_Image/iDS-2CD7A46G0-IZHSY_4MP_RightAngle45.png.thumb.1280.1280.png",
    ],
    "bullet-camera.jpeg": [
        "https://assets.hikvision.com/prd/normal/all/image/m000041483/筒机45-基线-4K-主图.png.thumb.1280.1280.png",
    ],
    "4mp-bullet-camera.jpeg": [
        "https://assets.hikvision.com/prd/normal/all/image/m000041483/筒机45-基线-4K-主图.png.thumb.1280.1280.png",
    ],
    "8mp-4k-bullet-camera.jpeg": [
        "https://assets.hikvision.com/prd/normal/all/image/m000041483/筒机45-基线-4K-主图.png.thumb.1280.1280.png",
    ],
    "thermal-camera.jpeg": [
        "https://www.hikvision.com/content/dam/hikvision/en/products/S000000001/S000000002/S000000003/S000000006/OFR000126/M000023964/Product_Image/DS-2TD2637B-10_P_RightAngle45.png.thumb.1280.1280.png",
    ],
    # NVRs
    "16-channel-nvr.jpeg": [
        "https://assets.hikvision.com/prd/normal/all/image/m000000574/MB-203Y-P-HIKVISION.png.thumb.1280.1280.png",
    ],
    "32-channel-4k-nvr.jpeg": [
        "https://assets.hikvision.com/prd/normal/all/image/m000000574/MB-203Y-P-HIKVISION.png.thumb.1280.1280.png",
    ],
    "64-channel-nvr.jpeg": [
        "https://assets.hikvision.com/prd/normal/all/image/m000000574/MB-203Y-P-HIKVISION.png.thumb.1280.1280.png",
    ],
    "kpoi-nvr.jpeg": [
        "https://assets.hikvision.com/prd/normal/all/image/m000000574/MB-203Y-P-HIKVISION.png.thumb.1280.1280.png",
    ],
    # HDDs
    "4tb-hdd.jpeg": [
        "https://www.seagate.com/www-content/product-content/skyhawk/ai-series/en-us/images/skyhawk-ai-20tb-3-5inch-helium-3yr-900x620.png",
        "https://www.westerndigital.com/content/dam/store/en-us/assets/products/internal-drives/wd-purple/wd-purple-10tb.png",
    ],
    "8tb-hdd.jpeg": [
        "https://www.seagate.com/www-content/product-content/skyhawk/ai-series/en-us/images/skyhawk-ai-20tb-3-5inch-helium-3yr-900x620.png",
    ],
    "16tb-hdd.jpeg": [
        "https://www.seagate.com/www-content/product-content/skyhawk/ai-series/en-us/images/skyhawk-ai-20tb-3-5inch-helium-3yr-900x620.png",
    ],
    # Switches
    "poe-switch.jpeg": [
        "https://www.hikvision.com/content/dam/hikvision/en/products/S000000001/S000000132/S000000149/S000000151/OFR000423/M000002994/Product_Image/DS-3E0510HP-E_RightSide.png.thumb.1280.1280.png",
    ],
    # Racks
    "18u-rack.png": [
        "https://static-assets.serverroom.net/2019/11/18u-server-rack.png",
    ],
    "22u-rack.png": [
        "https://static-assets.serverroom.net/2019/11/22u-server-rack.png",
    ],
    # Monitors
    "23-inch-monitor.jpeg": [
        "https://i.dell.com/sites/csimages/Video_Imagery/all/2408-monitor.png",
    ],
    "32-inch-tv-monitor.jpeg": [
        "https://i.dell.com/sites/csimages/Video_Imagery/all/3223q-monitor.png",
    ],
    # Workstation
    "dell-optiplex-with-8gb-ram-and-512ssd.jpeg": [
        "https://i.dell.com/sites/csimages/Product_Imagery/all/optiplex-7010-desktop.png",
    ],
    # UPS
    "2kva-rack-type-online-ups.jpeg": [
        "https://download.schneider-electric.com/files?p_Doc_Ref=SPD_STOS-7RSFVL_FS_V&p_File_Type=rendition_1500_jpg",
    ],
    # Accessories
    "hanging-stand-for-kpoi-camera.jpeg": [
        "https://www.hikvision.com/content/dam/hikvision/en/products/S000000001/S000000132/S000000150/S000000152/OFR000425/M000003011/Product_Image/DS-1275ZJ_RightSide.png.thumb.1280.1280.png",
    ],
    "48v-battery-cabinet-with-built-in-8-battery.jpeg": [
        "https://download.schneider-electric.com/files?p_Doc_Ref=SPD_STOS-7RSFVL_FS_V&p_File_Type=rendition_1500_jpg",
    ],
    "cat6-cable.jpeg": [
        "https://www.belden.com/-/media/product-images/10g-cables/cat6a-revolution-cable.ashx",
    ],
    "starfox-header.png": [
        "https://via.placeholder.com/800x200/1a237e/ffffff?text=STARFOX+SECURITY",
    ],
    "dell-logo.png": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Dell_Logo.png/800px-Dell_Logo.png",
    ],
    "hikvision-logo.png": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Hikvision_logo.svg/800px-Hikvision_logo.svg.png",
    ],
    "secuview-logo.jpeg": [
        "https://via.placeholder.com/300x80/003366/ffffff?text=SECUVIEW",
    ],
    "kstar-logo.jpeg": [
        "https://via.placeholder.com/300x80/004d40/ffffff?text=KSTAR",
    ],
    "toshiba-logo.jpeg": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Toshiba_logo.svg/800px-Toshiba_logo.svg.png",
    ],
    "kpoi-camera-lens.jpeg": [
        "https://assets.hikvision.com/prd/public/all/image/m000019593/右45°图.png.thumb.1280.1280.png",
    ],
    "2kva-ups-battery.jpeg": [
        "https://download.schneider-electric.com/files?p_Doc_Ref=SPD_STOS-7RSFVL_FS_V&p_File_Type=rendition_1500_jpg",
    ],
}


def download_image(url, filename):
    dest = IMG_DIR / filename
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"  SKIP {filename} (already exists)")
        return True
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "image/webp,image/png,image/jpeg,*/*",
        }
        r = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(dest, "wb") as f:
                f.write(r.content)
            print(f"  OK   {filename} ({len(r.content)} bytes)")
            return True
        else:
            print(f"  FAIL {filename} (status={r.status_code}, size={len(r.content)})")
            return False
    except Exception as e:
        print(f"  FAIL {filename} ({e})")
        return False


def main():
    print(f"Downloading product images to: {IMG_DIR}")
    print()

    for filename, urls in PRODUCTS.items():
        print(f"[{filename}]")
        success = False
        for url in urls:
            if download_image(url, filename):
                success = True
                break
        if not success:
            print(f"  !! No valid image downloaded for {filename}")
        print()


if __name__ == "__main__":
    main()
