import pandas as pd
import matplotlib.pyplot as plt


# read news topic percentage table
news_file = "../Topic classify/source_topic_statistics.csv"
news_df = pd.read_csv(news_file)

# read google trends summary table

trends_file = "../Google Trends/google_trends_summary.csv"
trends_df = pd.read_csv(trends_file)


news_df["percentage"] = news_df["percentage"].astype(str)
news_df["percentage"] = news_df["percentage"].str.replace("%", "")
news_df["percentage"] = news_df["percentage"].astype(float)

#restructure columns.
news_topic_percentage_table = news_df.pivot( index="category_topic",
                                             columns="source",
                                             values="percentage").reset_index()

#rename the columns:
news_topic_percentage_table = news_topic_percentage_table.rename(
    columns={"category_topic": "topic",
    "Reuters": "Reuters %",
    "Yahoo": "Yahoo %"})

#merge
comparison = news_topic_percentage_table.merge(trends_df, on="topic", how="left")


# rename google trends column 
comparison = comparison.rename(columns={"average_trend_score": "Google Trends Average"})


# final columns
comparison = comparison[["topic", "Reuters %", "Yahoo %", "Google Trends Average"]]


# sort by Google Trends score
comparison = comparison.sort_values("Google Trends Average",ascending=False)

#  Save final comparison table
comparison.to_csv("yahoo_reuters_google_trends_comparison.csv", index=False)

print("Saved: yahoo_reuters_google_trends_comparison.csv")


#create yahoo_reuters_google trends comparision chart

plot_df = comparison.set_index("topic")
bar = plot_df.plot(kind="bar", figsize=(12, 6))

for b in bar.containers:
    bar.bar_label(b,labels=[f"{value:.1f}" for value in b.datavalues],padding=2,fontsize=6)


plt.title("Yahoo, Reuters, and Google Trends Comparison, Apr 3–Apr 10, 2026")
plt.xlabel("Topic")
plt.ylabel("Value")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Data Source")
plt.tight_layout()

plt.savefig("yahoo_reuters_google_trends_comparison_chart.png")
plt.close()

print("Saved: yahoo_reuters_google_trends_comparison_chart.png")