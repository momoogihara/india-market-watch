import feedparser
from datetime import datetime

RSS_URLS = [
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best"
]
def fetch_articles_from_rss():
    articles = []
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published_at = None

            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_at = datetime(*entry.published_parsed[:6])

            articles.append({
                "title": entry.get("title", "No Title"),
                "content": (
                    entry.get("summary")
                    or entry.get("description")
                    or ""
                ),
                "source": url,
                "source_url": entry.get("link"),
                "published_at": published_at
            })
    return articles