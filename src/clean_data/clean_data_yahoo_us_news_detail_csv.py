import csv
from datetime import datetime
from pathlib import Path


input_csv = Path("yahoo_us_news_details.csv")
output_csv = Path("yahoo_us_news_details_clean.csv")

start_date = "2026-04-03"
end_date = "2026-04-10"

def clean_date(date_text: str) -> str:
        
        date_text = date_text.strip()
        
        # delete week
        date_part = date_text.split(",", 1)[1].strip()

        # Remove everything after "at"
        date_part = date_part.split(" at ")[0].strip()

        #change April 11, 2026
        date_part= datetime.strptime(date_part, "%B %d, %Y")

        #convert date format
        date_format = date_part.strftime("%Y-%m-%d")

        return date_format


with open(input_csv, "r") as f:

    reader = csv.DictReader(f)
    rows = list(reader)
    column_names = reader.fieldnames

clean_rows = []

for row in rows:
    row["publish_time"] = clean_date(row["publish_time"])
    if start_date <= row["publish_time"] <= end_date:
        clean_rows.append(row)

with open(output_csv, "w") as f:
    writer = csv.DictWriter(f, fieldnames=column_names)
    writer.writeheader()
    writer.writerows(clean_rows)


print("Clean Yahoo CSV saved to:", output_csv)