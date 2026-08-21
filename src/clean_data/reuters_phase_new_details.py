import csv
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup


file_path = Path("Reuters_html/reuters_2026_04/reuters_loaded.html")


output_csv = Path("Reuters_html") / "reuters_us_news_details.csv"

start_date = "2026-04-03"
end_date = "2026-04-10"


with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")


# Adjust the date format

def date_format(time_text: str) -> str:
    if not time_text:
        return ""

    time_text = time_text.strip()

    # skip:  mins ago , hours ago
    if "ago" in time_text.lower():
        return ""
    
    try:
        dt = datetime.strptime(time_text, "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return ""


# Find all news cards from HTML, and then place these news cards into the 'cards'list.

find_cards = 'li[data-testid="FeedListItem"]'
cards = soup.select(find_cards)

results = []
seen_urls = set()

for card in cards:
    
    # find title link form a and href
    title_link = card.select_one('a[data-testid="TitleLink"]')
    if not title_link:  
        title_link = card.find("a", href=True)

    if not title_link:
        continue

    href = title_link.get("href", "").strip()
    if not href:
        continue

    article_url = urljoin("https://www.reuters.com", href)

    if article_url in seen_urls:
        continue

    # title
    title = title_link.get_text(" ", strip=True)

    # time
    time_label = card.select_one('[data-testid="DateLineText"]')

    if time_label:
        time_text = time_label.get_text(" ", strip=True)
    else:
        time_text = ""

    publish_time = date_format(time_text)

    if not publish_time:
        continue
    if not (start_date <= publish_time <= end_date):
        continue

    # summary
    summary_label = card.select_one('[data-testid="Description"]')

    if summary_label:
        summary = summary_label.get_text(" ", strip=True)
    else:
        summary = ""


    seen_urls.add(article_url)
    results.append({"title": title,"publish_time": publish_time, "summary": summary, "article_url": article_url,})


# save CSV
with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["title", "publish_time", "summary", "article_url"]
    )
    writer.writeheader()
    writer.writerows(results)

print("Total feed cards saved:", len(results))
print("CSV saved to:", output_csv)

