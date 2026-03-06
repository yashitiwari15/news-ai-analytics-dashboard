import pandas as pd
import sqlite3
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

conn = sqlite3.connect("news.db")
df = pd.read_sql("SELECT * FROM news", conn)

model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = model.encode(df["title"].tolist())

k = 5
kmeans = KMeans(n_clusters=k)

df["topic"] = kmeans.fit_predict(embeddings)

df.to_sql("news", conn, if_exists="replace", index=False)

print("Topics generated successfully")