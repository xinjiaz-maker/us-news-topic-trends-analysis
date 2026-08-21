import csv
import time
import requests
from bs4 import BeautifulSoup

# 请求头
headers = {"User-Agent": "Mozilla/5.0"}

# 输入和输出文件名
input_csv = "yahoo_us_news_cards.csv"
output_csv = "yahoo_us_news_details.csv"


def parse_yahoo_us_news_detail(article_url):
    #parsing a new Detail page
    #retrun :url, title, summary, publish_time
    
    result = {
        "article_url": article_url,
        "title": "",
        "summary": "",
        "publish_time": ""
    }

    try:
        response = requests.get(article_url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        #title
        title = soup.find("h1")
        if title is not None:
            result["title"] = title.get_text(strip=True)

        #summary
        summary = soup.find("meta", attrs={"name": "description"})
        if summary is not None:
            result["summary"] = summary.get("content", "").strip()

        #time
        publish_time = soup.find("time")
        if publish_time is not None:
            result["publish_time"] = publish_time.get_text(strip=True)

    except Exception as error:
        print("=" * 80)
        print("Parsing Failed:", article_url)
        print("Error message:", error)

    return result


def read_urls_from_csv(file_path):

    #read all news links(url) from "yahoo_us_news_card.csv"
    
    urls = []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        print("original CSV list name:", reader.fieldnames)

        for row in reader:
            article_url = row.get("article_url", "").strip()
            if article_url != "":
                urls.append(article_url)

    return urls


def save_results_to_csv(results, file_path):
    
    #Save Detail Page Results to a New CSV
    
    with open(file_path, "w", encoding="utf-8-sig", newline="") as file:
        fieldnames = ["article_url", "title", "summary", "publish_time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)


def main():
    # 1. read all URLs
    article_urls = read_urls_from_csv(input_csv)
    print("Total number of URLs:", len(article_urls))

    # 2. parsing detail pages one by one
    all_results = []

    for url in article_urls:
        print("URL:", url)
        detail_data = parse_yahoo_us_news_detail(url)
        all_results.append(detail_data)
        time.sleep(1)

    # 3. save to new CSV
    save_results_to_csv(all_results, output_csv)
    print("=" * 80)
    print("detail page has alredy saved:", output_csv)


if __name__ == "__main__":
    main()