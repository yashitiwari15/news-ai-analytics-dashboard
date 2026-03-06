import pandas as pd
import sqlite3
from transformers import pipeline

conn = sqlite3.connect("news.db")
df = pd.read_sql("SELECT * FROM news", conn)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

summaries = []

for text in df["description"].fillna("").tolist():

    if len(text) > 50:
        summary = summarizer(text, max_length=40, min_length=10, do_sample=False)[0]["summary_text"]
    else:
        summary = text

    summaries.append(summary)

df["summary"] = summaries

df.to_sql("news", conn, if_exists="replace", index=False)

print("Summaries generated")