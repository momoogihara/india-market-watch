import feedparser
from datetime import datetime

RSS_URLS = [
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best"
]

def fetch_rss_articles():
    articles = []

    for url in RSS_URLS:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            article = {
                "title": entry.get("title"),
                "content": entry.get("summary", ""),
                "source": url,
                "published_at": entry.get("published", str(datetime.utcnow()))
            }
            articles.append(article)

    return articles

    