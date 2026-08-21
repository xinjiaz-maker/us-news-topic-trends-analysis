import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt


yahoo_file = "yahoo_us_news_details_clean.csv"
reuters_file = "reuters_us_news_details.csv"

yahoo = pd.read_csv(yahoo_file)
reuters = pd.read_csv(reuters_file)

# add source column
yahoo["source"] = "Yahoo"
reuters["source"] = "Reuters"

# combine two datasets
df = pd.concat([yahoo, reuters], ignore_index=True)


# create text column
df["text"] = df["title"]+ " " + df["summary"]
df["text_lower"] = df["text"].str.lower()

custom_stop_words = list(ENGLISH_STOP_WORDS.union([
    "said", "says", "new", "people", "year", "years",
    "friday", "thursday", "monday", "tuesday", "wednesday",
    "reuters", "yahoo", "cnn", "fox", "ap",
    "american", "americans", "according", "report", "reported",
    "news","to", "on", "of", "and", "in", "was", "he", "she", "his", "her", "with", "at", "after", "will"]))

# convert text into TF-IDF features（numbers）
Tfidf_vectorizer = TfidfVectorizer(stop_words=custom_stop_words, max_features=1000, min_df=4,max_df=0.7, ngram_range=(1, 2))

Tfidf_matrix = Tfidf_vectorizer.fit_transform(df["text"])


# Apply NMF topic modeling
number_topics = 8

NMF_model = NMF(n_components=number_topics, random_state=42, max_iter=500)

topic_matrix = NMF_model.fit_transform(Tfidf_matrix)


# Assign each article to its strongest NMF topic

df["nmf_topic_id"] = topic_matrix.argmax(axis=1)


# Print top keywords for each NMF topic

Feature_words = Tfidf_vectorizer.get_feature_names_out()

print(" NMF Topic Keywords: ")

for topic_id in range(number_topics):
    topic = NMF_model.components_[topic_id]
    used_words = []
    print("Topic", topic_id, ":")

    for rank in range(12):

        best_score = -1
        best_word = ""

        for i in range(len(Feature_words)):
            word = Feature_words[i]
            score = topic[i]
            if word not in used_words and score > best_score:
                best_score = score
                best_word = word
        used_words.append(best_word)

        print(best_word)

    print()

print(" Sample articles for each NMF topic: ")

for topic_id in range(number_topics):
    topic_articles = df[df["nmf_topic_id"] == topic_id]

    print("NMF Topic", topic_id)
    print("Number of articles:", len(topic_articles))







'''I use ketword-based to classify the topic'''

topic_keywords = {
    "Politics": 
        ["trump", "white house", "senate", "congress", "republican",
        "democrat", "election", "campaign", "administration",
        "governor", "lawmaker", "lawmakers", "biden", "vance",
        "committee", "desantis", "hegseth", "pentagon",
        "defense secretary", "secretary", "fema", "dhs", "doj",
        "mayor", "gov.", "sen.", "rep.", "representative",
        "political", "presidential run"],

    "Business": 
        ["inflation", "prices", "tariff", "tariffs", "trade",
        "economy", "economic", "market", "markets", "bank",
        "fed", "federal reserve", "powell", "consumer prices",
        "business", "stock", "stocks", "tax", "taxes",
        "gas bill", "farm machinery", "salespeople", "acquired",
        "company", "restaurant", "infrastructure", "fee",
        "h-1b visa fee", "cost", "spending"],

    "World news": 
        ["iran", "israel", "lebanon", "gaza", "ukraine", "russia",
        "china", "war", "military", "foreign", "diplomat",
        "diplomacy", "missile", "troops", "fighter", "ceasefire",
        "middle east", "u.k.", "uk", "terrorist", "jihad"],

    "Crime": 
        ["murder", "killed", "killer", "suspect", "arrested",
        "police", "charged", "death", "shooting", "shot",
        "missing", "attack", "attacked", "violence", "violent",
        "dead", "body", "crime", "criminal", "molotov",
        "strangler", "sexual misconduct", "sexual assault",
        "assault", "abuse", "abused", "rape", "raped",
        "sentenced", "prison", "kidnap", "minor", "locked",
        "thc", "alcohol", "under arrest", "gun", "drunk driver",
        "crash", "car crash", "house fire", "explosion",
        "injured", "injures", "vanished", "disappeared",
        "found", "frying pan", "bestiality", "accident",
        "vehicle", "interstate"],

    "Law": 
        ["court", "judge", "lawsuit", "justice", "legal",
        "trial", "attorney", "ruling", "probe", "investigation",
        "case", "charges", "charged", "appeal", "violated",
        "supreme court", "guilty", "pleaded guilty", "doj review",
        "law", "bill", "penalties"],

    "Education": 
        ["school", "student", "students", "college", "university",
        "campus", "teacher", "education", "board", "district",
        "classroom", "academic", "public library", "library"],

    "Science": 
        ["ai", "artificial intelligence", "openai", "meta",
        "youtube", "google", "tech", "technology", "software",
        "platform", "subscription", "social media", "nasa",
        "artemis", "astronauts", "moon mission", "space",
        "re-entry", "earth's atmosphere"],

    "Health": 
        ["health", "vaccine", "cdc", "hospital", "medical",
        "doctor", "disease", "patients", "drug", "medicine",
        "advisory panel", "drinking water", "pharmaceuticals",
        "microplastics", "epa"],

    "Environment": 
        ["climate", "pollution", "energy", "fuel", "gasoline",
        "oil", "emissions", "clean air", "environment",
        "environmental", "coal", "diesel", "whale",
        "endangered", "wildlife", "species"],

    "Immigration": 
        ["immigration", "immigrant", "migrant", "h-1b",
        "visa", "ice", "deportation", "asylum",
        "global talent", "citizenship and immigration services",
        "marines graduate", "ice fears"]}


def classify_topic(text):

    topic_scores = {}

    for topic in topic_keywords:
        keywords = topic_keywords[topic]

        score = 0

        for keyword in keywords:
            if keyword in text:
                score = score + 1

        topic_scores[topic] = score

    best_topic = max(topic_scores, key=topic_scores.get)
    best_score = topic_scores[best_topic]

    if best_score == 0:
        return "Other"
    else:
        return best_topic

# creat category topc and save to csv

df["category_topic"] = df["text_lower"].apply(classify_topic)

df.to_csv("news_with_category_topics.csv", index=False)

print(" Saved: news_with_category_topics.csv")


#create summary table

#1.Count the number of articles for each category topic under each news source.
group = (df.groupby(["source", "category_topic"]))

topic_count = group.size()
topic_count = topic_count.reset_index(name="article_count")

#2.Count the total news of yahoo , the total news of reuters.
source_group= df.groupby("source")

source_total = source_group.size()
source_total = source_total.reset_index(name="total_articles")

# merge aricle_count and total_articles into a csv
topic_summary = topic_count.merge(source_total, on="source")

#calculate the percentage
topic_summary["percentage"] = (topic_summary["article_count"] / topic_summary["total_articles"] * 100).round(2)
topic_summary["percentage"] = topic_summary["percentage"].astype(str) + "%"


topic_summary = topic_summary.sort_values(["source", "article_count"],ascending=[True, False])

#Used to compare the reporting proportions of Yahoo and Reuters across different news topics.
topic_summary.to_csv("source_topic_statistics.csv", index=False)

print("Saved: source_topic_statistics.csv.csv")


# create yahoo vs reuters topic percentage bar chart

topic_summary["percentage_number"] = topic_summary["percentage"].str.replace("%", "")
topic_summary["percentage_number"] = topic_summary["percentage_number"].astype(float)

plot_df = topic_summary.pivot(index="category_topic", 
                              columns="source",
                              values="percentage_number")

plt.figure(figsize=(10, 6))
bar = plot_df.plot(kind="bar", figsize=(11, 6))

for b in bar.containers:
    bar.bar_label(b, labels=[f"{value:.2f}%" for value in b.datavalues],padding=3,fontsize=8)
    
plt.title("Yahoo vs Reuters Topic Percentage Comparison, Apr 3–Apr 10, 2026")
plt.xlabel("Topic")
plt.ylabel("Percentage of Articles (%)")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Source")
plt.tight_layout()
plt.savefig("yahoo_reuters_topic_percentage_comparison.png")
plt.show()

print("Saved: yahoo_reuters_topic_percentage_comparison.png")