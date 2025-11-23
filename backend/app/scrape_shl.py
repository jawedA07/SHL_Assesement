import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin
from tqdm import tqdm

BASE = "https://www.shl.com/solutions/products/product-catalog/"

def get_listing_pages(start_url=BASE, max_pages=200):
    visited = set()
    to_visit = [start_url]
    product_links = set()
    headers = {"User-Agent":"Mozilla/5.0 (compatible; SHLRecommender/1.0)"}

    pbar = tqdm(total=max_pages, desc="Crawling listing pages", unit="page")
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print("Failed to fetch", url, e)
            continue
        visited.add(url)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a['href']
            if "/products/" in href or "/solutions/" in href:
                full = urljoin(url, href)
                product_links.add(full)

        for a in soup.find_all("a", href=True):
            txt = a.get_text(strip=True).lower()
            if txt in ("next", ">", "more"):
                full = urljoin(url, a['href'])
                if full not in visited:
                    to_visit.append(full)

        pbar.update(1)
        time.sleep(0.5)
    pbar.close()
    return list(product_links)

def parse_product_page(url):
    headers = {"User-Agent":"Mozilla/5.0 (compatible; SHLRecommender/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("h1")
    title_text = title.get_text(strip=True) if title else ""
    p = soup.find("p")
    desc = p.get_text(strip=True) if p else ""
    meta = []
    for span in soup.find_all(["span","li","div"]):
        cls = span.get("class")
        if cls and ("product-type" in " ".join(cls) or "category" in " ".join(cls)):
            meta.append(span.get_text(strip=True))
    return {"name": title_text, "url": url, "description": desc, "meta": " | ".join(meta)}

def main():
    print("Start crawling SHL catalog. This can take several minutes.")
    product_links = get_listing_pages()
    print(f"Found {len(product_links)} candidate links. Filtering and parsing...")
    rows = []
    for link in tqdm(product_links):
        res = parse_product_page(link)
        if not res:
            continue
        n = res['name'].lower()
        if "pre-packaged" in n or "pre packaged" in n or "job solution" in n.lower():
            continue
        if len(res['name'].strip()) < 3:
            continue
        rows.append(res)
    unique = {}
    for r in rows:
        key = (r['name'].strip(), r['url'].strip())
        unique[key] = r

    out_file = "data/shl_catalog.csv"
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name","url","description","meta"])
        writer.writeheader()
        for r in unique.values():
            writer.writerow(r)
    print(f"Saved {len(unique)} items to {out_file}")

if __name__ == "__main__":
    main()
