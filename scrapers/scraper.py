import httpx
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from urllib.parse import urlencode
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


def _get_proxy_url(url):
    payload = {"api_key": API_KEY, "url": url}
    return f"https://proxy.scrapeops.io/v1/?{urlencode(payload)}"


def _get_html(client: httpx.Client, url: str) -> HTMLParser:
    response = client.get(url, timeout=None)
    response.raise_for_status()
    return HTMLParser(response.text)


update_data = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X "
                  "10_15_7) AppleWebKit/537.36 (KHTML, "
                  "like Gecko) Chrome/119.0.0.0 "
                  "Safari/537.36"}


def get_html_tree_for(url: str) -> HTMLParser:
    proxy_url = _get_proxy_url(url)

    with httpx.Client() as client:
        client.headers.update(update_data)
        return _get_html(client, proxy_url)
