
## 1.Project Overview:
This project compares U.S. news topic trends on Yahoo News and Reuters during the period from April 3 to April 10, 2026, and then examining whether those highlighted topics also aligned with broader public interest on Google Trends.

The project focuses on four research questions:

1. What types of topics appear most frequently on the U.S. pages of Yahoo News and Reuters?
2. How did topic coverage differ between Yahoo News and Reuters?
3. Do the topics highlighted by these two platforms also align with broader public interest as reflected in Google Trends?
4. Which topics show the largest gap between media coverage and public interest?

## 2.Requirements
Main libraries used in this project:

- `pandas`: data cleaning, merging, grouping, and analysis
- `requests`: sending requests to web pages
- `beautifulsoup4`: parsing HTML content
- `scikit-learn`: TF-IDF and NMF topic modeling
- `matplotlib`: creating visualizations


## 3.Data Sources
### 3.1 Yahoo News U.S.
URL:https://news.yahoo.com/us/
Collected fields: title， publish_time， summary， article_url
Final cleaned file: yahoo_us_news_details_clean.csv

### 3.2 Reuters U.S. News
URL:https://www.reuters.com/world/us/
Collected fields: title， publish_time， summary， article_url
Final cleaned file: reuters_us_news_details.csv

### 3.3 Google Trends
The Google Trends data was downloaded manually as CSV files for the following topic categories:
Business
Crime
Education
Environment
Health
Immigration
Law
Politics
Science
World news

## 4. How to get the data
### 4.1 Yahoo News and Reuters Data
Yahoo News data was collected using Python with `requests` and `BeautifulSoup`. The Yahoo data collection process used three scripts. First, `download_html_yahoo_pages.py` requested Yahoo News U.S. list pages and saved the HTML content locally. Then `yahoo_parse_list_page.py` used `BeautifulSoup` to parse the saved list-page HTML files and extract article links from the news cards. After that, `yahoo_parse_detail_page.py`and `clean_data_yahoo_us_news_detail_csv.py `opened each article link and extracted detailed article-level information, including title, summary, publication time, and article URL. The final cleaned Yahoo dataset used in the analysis was saved as `yahoo_us_news_details_clean.csv`, which contains `title`, `publish_time`, `summary`, and `article_url`.

Reuters data was collected from saved HTML. I first opened the Reuters U.S. news page in the browser and copied the loaded HTML content. Then `reuters_local_parse.py` used `BeautifulSoup` to parse the saved HTML and extract basic article information, such as article links, titles, summaries, and time information. After that, `reuters_phase_new_details.py` cleaned and standardized the extracted data and saved the final Reuters dataset as `reuters_us_news_details.csv`. The final file contains `title`, `publish_time`, `summary`, and `article_url`.

### 4.2 Google Trends
I manually searched comparable topic terms based on the topic categories used in the news classification and downloaded the trend data as CSV files:
    business.csv
    crime.csv
    education.csv
    environment.csv
    health.csv
    immigration.csv
    law.csv
    politics.csv
    science.csv
    world news.csv
Exach csv contains : Time, topic score

## 5. How to clean the data
The Yahoo News and Reuters datasets were cleaned and standardized before analysis.

Cleaning steps included:

1. Removing incomplete records
2. Standardizing column names
3. Converting different date formats into a consistent YYYY-MM-DD format
4. Filtering articles to the selected period from April 3 to April 10, 2026
5. Adding a source column to identify whether an article came from Yahoo or Reuters
6. Combining title and summary into one text field for topic classification
After cleaning, both Yahoo and Reuters datasets had the same structure:
`title`, `publish_time`, `summary`, and `article_url`.

## 6. How to run Topic Classification
The topic classification script is:
`NMF_exploratory_Keyword_based_classification.py`
1. Read the cleaned Yahoo and Reuters CSV files
`yahoo_us_news_details_clean.csv`
`reuters_us_news_details.csv`
2. Add a source column to each dataset
3. Combines the Yahoo and Reuters datasets into one Dataframe
4. Creat a text column title + summary
5. Applies NMF topic modeling as an exploratory step
6. Applies keyword-based classification for the final topic labels
7. Assigns each article to a topic category
`Politics`, `Education`,`Crime`,`Business`,`Health`,`law`,`Immigration`,`Science`,`World news`,`Environment`
8. Calculates topic article counts by source
9. Calculates topic percentages by source
10. Generates the Yahoo vs Reuters topic percentage chart

Main output files:
`news_with_category_topics.csv`
`source_topic_statistics.csv`
`yahoo_reuters_topic_percentage_comparison.png`

## 7.How to Run Google Trends Analysis
The Google Trends analysis script is:
`google_trends_analysis.py`
1. Reads all Google Trends CSV files
2. Filters the data to April 3 to April 10, 2026
3. Calculates the average Google Trends score for each topic
4. Saves the Google Trends summary table
5. Creates a bar chart of average public search interest by topic

Main output files:
`google_trends_summary.csv`
`google_trends_topic_average.png`

## 8.How to Compare Yahoo, Reuters with Google Trends
The comparison script is:
`create_news_google_comparison_table.py`
This script merges:
`source_topic_statistics.csv`
`google_trends_summary.csv`
Main output files:
`yahoo_reuters_google_trends_comparison.csv`
The script also generates:
`news_google_trends_comparison_chart.png`
This figure compares Yahoo, Reuters, and Google Trends in one grouped bar chart.

## 9.Visualizations
The visualizations were created using Python libraries such as pandas, matplotlib. pandas was used to read and prepare the CSV files, while matplotlib were used to create bar charts for comparing topic percentages and Google Trends scores.

This project produces three main visualizations.
### 9.1 Yahoo vs Reuters Topic Percentage Comparison
File: `yahoo_reuters_topic_percentage_comparison.png`
Input file: `source_topic_statistics.csv`
This figure compares the percentage of articles in each topic category for Yahoo News and Reuters.
X-axis: topic categories
Y-axis: percentage of articles
Bars: Yahoo and Reuters

### 9.2 Average Google Trends Public Interest by Topic
File: `google_trends_topic_average.png`
Input file: `google_trends_summary.csv`
This figure shows the average Google Trends search interest score for each topic from April 3 to April 10, 2026.
X-axis: topic categories
Y-axis: average Google Trends score
Google Trends scores are relative search interest scores, not raw search counts.

### 9.3 Yahoo, Reuters, and Google Trends Comparison
File: `yahoo_reuters_google_trends_comparison_chart.png`
Input file: `yahoo_reuters_google_trends_comparison.csv`
This figure combines:
Reuters topic coverage percentage
Yahoo topic coverage percentage
Google Trends average score
This chart is used to compare media coverage with public search interest.
