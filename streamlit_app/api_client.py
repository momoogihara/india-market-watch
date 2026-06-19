import requests

BASE_URL = "http://api:8000"

def get_articles():
    res = requests.get(f"{BASE_URL}/articles")
    return res.json()

def get_market_reports():
    res = requests.get(f"{BASE_URL}/market-report/history")
    return res.json()

def generate_report():
    res = requests.get(f"{BASE_URL}/market-report/generate")
    return res.json()

def import_rss():
    response = requests.post(f"{BASE_URL}/articles/import-rss")
    response.raise_for_status()
    return response.json()

def get_market_snapshot():
    return requests.get(
        f"{BASE_URL}/articles/market-snapshot"
    ).json()


def get_top_sectors():
    return requests.get(
        f"{BASE_URL}/articles/top-sectors"
    ).json()


def get_market_trends():
    return requests.get(
        f"{BASE_URL}/articles/market-trends"
    ).json()