import json

import httpx
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from urllib.parse import urlencode
import os


# -------------------------------------------------------
# Proxy URL is provided by ScrapeOps
# license lasts 30 days
# Credit limit: 1,000
# a single run of the scraper uses 208 credits
#
#  BUILD THE PROXY URL
# -------------------------------------------------------

def get_html() -> HTMLParser:
    with open("data/scraped.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    main_page = HTMLParser(html_content)

    accordions = main_page.css_first("div#afghanistan address")
    if accordions:
        return accordions.text(strip=True)
    return "none found"



