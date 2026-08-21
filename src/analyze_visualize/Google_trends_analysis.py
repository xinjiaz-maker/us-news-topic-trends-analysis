import pandas as pd
import matplotlib.pyplot as plt

google_trends_data_files = {"Business": "business.csv",
    "Crime": "crime.csv",
    "Education": "education.csv",
    "Environment": "environment.csv",
    "Health": "health.csv",
    "Immigration": "immigration.csv",
    "Law": "law.csv",
    "Politics": "politics.csv",
    "Science": "science.csv",
    "World news": "world news.csv"}

start_date = "2026-04-03"
end_date = "2026-04-10"

results = []

#filter the time 4.3-4.10
for topic_name, file_name in google_trends_data_files.items():
    df = pd.read_csv("Google trends data/" + file_name)
    df["Time"] = pd.to_datetime(df["Time"])

    filtered_time = df[(df["Time"] >= start_date) &(df["Time"] <= end_date)]
    score_column = df.columns[1]

#calcuate google trends each topics average
    average_score = round(filtered_time[score_column].mean())

    results.append({"topic": topic_name, "average_trend_score": average_score})

'''Organize the previously collected average Google Trends results into a table,
sort them in descending order of popularity, 
and then save the result as a CSV file.'''
    
google_trends_summary = pd.DataFrame(results)
google_trends_summary = google_trends_summary.sort_values("average_trend_score",ascending=False)

google_trends_summary.to_csv("google_trends_summary.csv", index=False)

print("Saved: google_trends_summary.csv")

#create bar chart

bar = google_trends_summary.plot(x="topic", y="average_trend_score", kind="bar", figsize=(10, 6),
    legend=False)

for b in bar.containers:
    bar.bar_label(b, labels=[f"{value:.0f}" for value in b.datavalues],padding=3,fontsize=8)

plt.xlabel("Topic")
plt.ylabel("Average Google Trends Score")
plt.title("Average Google Trends Public Interest by Topic, Apr 3–Apr 10, 2026")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("google_trends_topic_average.png")
plt.show()