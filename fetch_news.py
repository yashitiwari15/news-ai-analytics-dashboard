
import requests
import pandas as pd

API_KEY = "3b22b9a0717b4d85a68e6da8eed84010"

url = f"https://newsapi.org/v2/everything?q=india&language=en&sortBy=publishedAt&pageSize=50&apiKey={API_KEY}"

response = requests.get(url)
data = response.json()

print("Total Results:", data["totalResults"])

articles = data.get("articles", [])

if len(articles) == 0:
    print("No articles returned from API")
else:
    a = []

    for i in articles:
        a.append({
            "source": i["source"]["name"],
            "title": i["title"],
            "description": i["description"],
            "published": i["publishedAt"]
        })

    df = pd.DataFrame(a)

    df.to_csv("data/news_raw.csv", index=False)

    print("News data collected successfully")

