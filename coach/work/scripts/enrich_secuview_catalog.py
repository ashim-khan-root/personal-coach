import csv
import re
import sys
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

def get_soup(url, retries=3):
    for attempt in range(retries):
        try:
            resp = SESSION.get(url, timeout=20)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)

in_path = sys.argv[1] if len(sys.argv) > 1 else "work/content/secuview-facebook-catalog.csv"
out_path = in_path

with open(in_path) as f:
    rows = list(csv.DictReader(f))

total = len(rows)
for i, row in enumerate(rows):
    url = row["link"]
    needs_desc = not row.get("description", "").strip()
    needs_img = not row.get("image_link", "").strip()
    if not needs_desc and not needs_img:
        continue

    print(f"  [{i+1}/{total}] {row['id']}", file=sys.stderr)
    try:
        soup = get_soup(url)

        if needs_img:
            img_el = soup.find("img", class_="wp-post-image")
            if img_el:
                row["image_link"] = img_el.get("src") or ""

        if needs_desc:
            after = soup.find("div", class_="electron-row-after-summary")
            desc = ""
            if after:
                desc = after.get_text(strip=True)[:2000]
            if not desc:
                short = soup.find("div", class_="electron-summary-item")
                if short:
                    dd = short.find("div")
                    if dd:
                        desc = dd.get_text(strip=True)[:2000]
            row["description"] = desc

    except Exception as e:
        print(f"  FAIL: {e}", file=sys.stderr)

    time.sleep(0.8)

fields = ["id", "title", "description", "availability", "condition",
          "price", "link", "image_link", "brand", "google_product_category"]
with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

with_desc = sum(1 for r in rows if r.get("description","").strip())
with_img = sum(1 for r in rows if r.get("image_link","").strip())
print(f"\nDone! {total} rows. With desc: {with_desc}, With img: {with_img}", file=sys.stderr)
