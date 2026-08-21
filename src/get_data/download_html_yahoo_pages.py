#download yahoo page 1-20 html
import os
import time
import requests

request_headers = {"User-Agent": "Mozilla/5.0"}

# save the name of the folder for saving HTML files.
save_folder_name = "yahoo_html"

# Download from page 1 to page 20.
for page_number in range(1, 21):

    # The URL for the first page differs from the URLs for subsequent pages.
    #page 1 "https://www.yahoo.com/news/us/"
    #page 2 "https://www.yahoo.com/news/us/2/"
    if page_number == 1:
        page_url = "https://www.yahoo.com/news/us/"
    else:
        page_url = "https://www.yahoo.com/news/us/" + str(page_number) + "/"

    print("Now downloading page", page_number)
    print("Page URL:", page_url)

    try:
        response = requests.get(page_url, headers=request_headers, timeout=20)

        print("Status code:", response.status_code)

        response.raise_for_status()

        response.encoding = "utf-8"

        # set file name"yahoo_us_page_1""yahoo_us-page_2"
        file_name = "yahoo_us_page_" + str(page_number) + ".html"

        # Construct the complete save path.
        file_path = os.path.join(save_folder_name, file_name)

        # Write HTML to a local file.
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)

        print("Saved successfully:", file_path)
        print("HTML length:", len(response.text))
        print("-" * 50)

    except Exception as error:
        print("This page failed:", page_number)
        print("Error message:", error)
        print("-" * 50)

    # pause for 1.5
    time.sleep(1.5)

print("All pages finished.")