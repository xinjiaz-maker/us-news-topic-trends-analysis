from bs4 import BeautifulSoup
from urllib.parse import urljoin

file_path = "reuters_html/reuters_2026_04_04_page1.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

tags = soup.find_all("a", href=True)

urls = []
seen = set()

for tag in tags:
    href = tag["href"]

    if "/world/us/" in href:
        full_url = urljoin("https://www.reuters.com", href)

        if full_url not in seen:
            seen.add(full_url)
            urls.append(full_url)

print("Reuters US links found:\n")

for i, url in enumerate(urls, 1):
    print(f"{i}. {url}")

print(f"\nTotal unique Reuters US links: {len(urls)}")