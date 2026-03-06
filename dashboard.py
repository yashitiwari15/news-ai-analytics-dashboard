import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time

# Page config
st.set_page_config(page_title="AI News Intelligence Dashboard", layout="wide")

st.title("AI News Intelligence Dashboard")

st.markdown(
    "Interactive analytics platform for monitoring news trends, sentiment, and AI-driven insights."
)

# Database connection
conn = sqlite3.connect("news.db")
df = pd.read_sql("SELECT * FROM news", conn)

# Sidebar filters
st.sidebar.header("Dashboard Filters")

sources = st.sidebar.multiselect(
    "Select News Sources",
    df["source"].unique(),
    default=df["source"].unique()
)

df = df[df["source"].isin(sources)]

st.sidebar.write("Articles Selected:", len(df))

# Refresh button
if st.sidebar.button("🔄 Refresh Dashboard"):
    st.experimental_rerun()

# ---------------- KPI METRICS ----------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Articles", len(df))
col2.metric("Unique Sources", df["source"].nunique())
col3.metric("Average Sentiment", round(df["sentiment"].mean(), 2))

st.divider()

# ---------------- SOURCE DISTRIBUTION ----------------

st.subheader("Top News Sources")

source_counts = df["source"].value_counts().reset_index()
source_counts.columns = ["source", "count"]

fig_sources = px.bar(
    source_counts,
    x="source",
    y="count",
    color="count",
    title="Articles by Source",
)

st.plotly_chart(fig_sources, use_container_width=True)

# ---------------- SENTIMENT ANALYSIS ----------------

st.subheader("Sentiment Trend Over Time")

fig_sentiment = px.scatter(
    df,
    x="date",
    y="sentiment",
    color="source",
    title="News Sentiment Timeline"
)

st.plotly_chart(fig_sentiment, use_container_width=True)

# ---------------- PUBLISHING TREND ----------------

st.subheader("News Publishing Trend")

trend = df.groupby("date").size().reset_index(name="articles")

fig_trend = px.line(
    trend,
    x="date",
    y="articles",
    markers=True,
    title="Articles Published Over Time"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ---------------- 3D ARTICLE ANALYTICS ----------------

st.subheader("3D News Analytics")

fig3d = px.scatter_3d(
    df,
    x="sentiment",
    y="source",
    z="topic",
    color="topic",
    title="3D Article Distribution by Topic"
)

st.plotly_chart(fig3d, use_container_width=True)

# ---------------- TOPIC DISTRIBUTION ----------------

st.subheader("AI Topic Detection")

topic_counts = df["topic"].value_counts().reset_index()
topic_counts.columns = ["topic", "articles"]

fig_topic = px.pie(
    topic_counts,
    names="topic",
    values="articles",
    title="Topic Distribution"
)

st.plotly_chart(fig_topic, use_container_width=True)

# ---------------- WORD CLOUD ----------------

st.subheader("Trending Keywords")

text = " ".join(df["title"].astype(str))

wordcloud = WordCloud(
    width=900,
    height=400,
    background_color="white"
).generate(text)

fig_wc, ax = plt.subplots()

ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig_wc)

# ---------------- AI SUMMARIES ----------------

st.subheader("AI Generated News Summaries")

if "summary" in df.columns:

    for i, row in df.head(5).iterrows():

        st.markdown("### " + row["title"])
        st.write(row["summary"])
        st.divider()

# ---------------- DATASET EXPLORER ----------------

st.subheader("Dataset Explorer")

st.dataframe(df, use_container_width=True)