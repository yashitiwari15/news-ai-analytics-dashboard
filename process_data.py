import pandas as pd
from textblob import TextBlob
import sqlite3

df = pd.read_csv("data/news_raw.csv")

df = df.dropna()

def sentiment(x):
    return TextBlob(x).sentiment.polarity

df["sentiment"] = df["title"].apply(sentiment)

df["date"] = pd.to_datetime(df["published"]).dt.date

conn = sqlite3.connect("news.db")

df.to_sql("news", conn, if_exists="replace", index=False)

print("Data processed successfully")