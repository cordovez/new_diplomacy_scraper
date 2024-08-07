import httpx
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from urllib.parse import urlencode
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


# -------------------------------------------------------
# Proxy URL is provided by ScrapeOps
# license lasts 30 days
# Credit limit: 1,000
# a single run of the scraper uses 208 credits
#
#  BUILD THE PROXY URL
# -------------------------------------------------------

def _fetch_by_proxy(client: httpx.Client, url: str) -> HTMLParser:
    """
    Fetches the content of a URL using an HTTP client and returns an HTMLParser object.

    Args:
        client: The HTTP client used to make the request.
        url: The URL to fetch the content from.

    Returns:
        An HTMLParser object containing the parsed content of the fetched URL.
    """
    response = client.get(url, timeout=None)
    response.raise_for_status()
    return HTMLParser(response.text)


def scrape_html_tree_for(url) -> HTMLParser:
    """
    Scrapes the HTML content of a URL using a proxy and saves it to a file.

    Args:
        url: The URL to scrape the HTML content from.

    Returns:
        An HTMLParser object representing the scraped HTML content.
    """
    payload = {"api_key": API_KEY, "url": url}
    proxy_url = f"https://proxy.scrapeops.io/v1/?{urlencode(payload)}"
    update_data = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X "
                      "10_15_7) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Chrome/119.0.0.0 "
                      "Safari/537.36"}

    with httpx.Client() as client:
        client.headers.update(update_data)
        response = _fetch_by_proxy(client, proxy_url)

    with open("data/scraped.html", "w") as file:
        file.write(response.html)

    return response


def _load_html_from_file(filepath: str) -> HTMLParser:
    """
    Loads HTML content from a file and returns an HTMLParser object.

    Args:
        filepath: The path to the file containing the HTML content.

    Returns:
        An HTMLParser object representing the content loaded from the file.
    """
    with open(filepath, "r") as file:
        html_content = file.read()
    return HTMLParser(html_content)


def scrape_or_read_from_file() -> HTMLParser:
    """
        Checks if a file with scraped HTML content exists, and either loads it or
        scrapes a new page.

        Returns:
            An HTMLParser object representing the scraped or loaded HTML content.
        """
    if os.path.exists("data/scraped.html"):
        return _load_html_from_file("data/scraped.html")

    main_page = "https://www.ireland.ie/en/dfa/embassies/"
    return scrape_html_tree_for(main_page)
