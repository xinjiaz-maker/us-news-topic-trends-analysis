import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# used to store url that have alreay appear, and preventing repeat of entire page.
urls_repeated = set()

# count the total number of us news
us_news_count = 0

#save all filtered news results and then store in CSV format.
all_news = []

# from page 1 to page 20, process them one by one
for page_number in range(1, 21):
    file_path = f"yahoo_html/yahoo_us_page_{page_number}.html"

    # Read the HTML file for this page
    with open(file_path, "r", encoding="utf-8") as file:
        yahoo_html = file.read()

    # parse HTML
    soup = BeautifulSoup(yahoo_html, "html.parser")

    # Find all div areas on the webpage
    all_areas = soup.find_all("div")

    print(f"start inspect page {page_number}")

    # inspect div one by one
    for one_area in all_areas:
        #take all visible text
        text_area = one_area.get_text(" ", strip=True)

        # condition 1：This text must begin with "US"
        start_us = text_area.startswith("US ")

        # condition 2：This text must begin with "US"
        starts_ad = text_area.startswith("AD ")

        # Find all <a> tags with links in this area
        all_links = one_area.find_all("a", href=True)

        # store links to articles found in this area
        urls = []

        # inspect link one by one
        for one_link in all_links:
            href = one_link["href"]

            # only keep the article link
            if "/news/articles/" in href:
                # Complete the half link
                full_url = urljoin("https://www.yahoo.com", href)
                # Avoid adding the same link multiple times within the same area
                if full_url not in urls:
                    urls.append(full_url)

        # condition 3：A news card must contain exactly one article link
        only_one_url = len(urls) == 1

        # give article_url none first
        article_url = None

        # If this area only have one article link, extract it.
        if only_one_url:
            article_url = urls[0]

        # condition 4：This link cannot be repeat of one that has already been extract
        not_repeated = False
        if article_url is not None and article_url not in urls_repeated:
            not_repeated = True

    
        # If all conditions are met, print it out
        if start_us and not starts_ad and only_one_url and not_repeated:
            urls_repeated.add(article_url)
            us_news_count = us_news_count + 1

            print("this is", us_news_count, "us card")
            print("From page:", page_number)
            print("card number:")
            print(text_area)
            print("full_url_link:")
            print(article_url)
            print("-" * 80)

            news_item = { "news_number": us_news_count,
                         "page_number": page_number,
                         "card_text": text_area,
                         "article_url": article_url}
            all_news.append(news_item)

print("The total number of US news cards screened is:", us_news_count)

with open("yahoo_us_news_cards.csv", "w", newline="", encoding="utf-8") as file:

    first_line_names = ["news_number", "page_number", "card_text", "article_url"]
    writer = csv.DictWriter(file, fieldnames=first_line_names)
    writer.writeheader()
    writer.writerows(all_news)

print("CSV file is already saved: yahoo_us_news_cards.csv")