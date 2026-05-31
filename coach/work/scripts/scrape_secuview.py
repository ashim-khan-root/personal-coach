import csv
import re
import sys
import time
import requests
from bs4 import BeautifulSoup

BASE = "https://secuview.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
DELAY = 1.0

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
            print(f"  RETRY [{attempt+1}/{retries}] {e}", file=sys.stderr)
            time.sleep(2 ** attempt)

def find_product_urls():
    urls = set()
    sources = ["/shop-page/", "/all-products/"]
    # Find category links from homepage
    soup = get_soup(BASE)
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if "/product-category/" in h:
            sources.append(h)
    sources = list(set(sources))
    for src in sources:
        try:
            s = get_soup(src if src.startswith("http") else BASE + src)
            for a in s.find_all("a", href=True):
                h = a["href"]
                if "/product/" in h and h.count("/") >= 4:
                    urls.add(h.split("?")[0].split("#")[0])
        except:
            pass
        time.sleep(DELAY)
    return sorted(urls)

def extract_categories(body_class):
    m = re.findall(r'product_cat-([\w-]+)', body_class)
    return " > ".join(m) if m else ""

def scrape_product(url):
    soup = get_soup(url)
    body = soup.find("body")
    body_class = " ".join(body.get("class", [])) if body else ""

    title_el = soup.find("h1", class_="product_title") or soup.find("h1")
    title = title_el.get_text(strip=True) if title_el else ""

    sku = ""
    meta = soup.find("div", class_="electron-meta-wrapper")
    if meta:
        sku_text = meta.get_text(strip=True)
        sku = sku_text.replace("SKU:", "").strip()
    if not sku:
        m = re.search(r'SKU:\s*(\S+)', soup.get_text())
        if m:
            sku = m.group(1)

    price = ""
    price_el = soup.find("span", class_="woocommerce-Price-amount")
    if price_el:
        raw = price_el.get_text(strip=True)
        raw = raw.replace(",", "")
        m = re.search(r'([\d.]+)', raw)
        if m:
            price = m.group(1)

    availability = "in stock"
    meta_prop = soup.find("meta", {"property": "product:availability"})
    if meta_prop:
        availability = meta_prop.get("content", "in stock")

    img = ""
    img_el = soup.find("img", class_="wp-post-image")
    if img_el:
        img = img_el.get("src") or ""

    after_summary = soup.find("div", class_="electron-row-after-summary")
    description = ""
    if after_summary:
        description = after_summary.get_text(strip=True)[:2000]
    if not description:
        short = soup.find("div", class_="electron-summary-item")
        if short:
            desc_div = short.find("div")
            if desc_div:
                description = desc_div.get_text(strip=True)[:2000]

    category = extract_categories(body_class)

    return {
        "id": sku or title[:20],
        "title": title,
        "description": description,
        "availability": availability,
        "condition": "new",
        "price": price,
        "link": url,
        "image_link": img,
        "brand": "Secuview",
        "google_product_category": category,
    }

def main():
    print("Step 1: Finding all product URLs...", file=sys.stderr)
    urls = find_product_urls()
    print(f"Found {len(urls)} unique product URLs", file=sys.stderr)

    products = []
    for i, url in enumerate(urls, 1):
        print(f"  [{i}/{len(urls)}] {url}", file=sys.stderr)
        try:
            prod = scrape_product(url)
            products.append(prod)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
        time.sleep(DELAY)

    out_path = sys.argv[1] if len(sys.argv) > 1 else "secuview-facebook-catalog.csv"
    fields = ["id", "title", "description", "availability", "condition",
              "price", "link", "image_link", "brand", "google_product_category"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(products)

    print(f"\nDone! {len(products)} products saved to {out_path}", file=sys.stderr)
    for p in products:
        print(f"  {p['id']:30s} | {p['price']:>8s} | {p['title'][:55]}")

if __name__ == "__main__":
    main()
