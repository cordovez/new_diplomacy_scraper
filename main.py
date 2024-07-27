import httpx
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from urllib.parse import urlencode
import os
from rich import print

from services import extract
from scrapers.scraper import get_html_tree_for
from services.extract import presence_status
#
# load_dotenv()
# API_KEY = os.getenv("API_KEY")
#
#
# def get_proxy_url(url):
#     payload = {"api_key": API_KEY, "url": url}
#     return f"https://proxy.scrapeops.io/v1/?{urlencode(payload)}"
#
#
# def get_html(client: httpx.Client, url: str) -> HTMLParser:
#     response = client.get(url, timeout=None)
#     response.raise_for_status()
#     return HTMLParser(response.text)


def parse_landing_page(html_tree: HTMLParser) -> list[dict]:
    data = []
    count = 0
    for accordion in html_tree.css(".accordion"):
        count: count
        div_id: str = accordion.attributes["id"]
        accordion_title: str = accordion.css_first(
            "span.embassy_accordion__title").text().strip()
        group_index: str = accordion.attributes["accordian"]  # the misspelling is in
        # html

        if content_node := accordion.css_first(f"#answer-{group_index}"):
            first_h2: str = extract.h2(content_node)
            first_h3: str = extract.h3(content_node)
            hosts_emb: bool = extract.presence_status(content_node)
            address = extract.address(content_node)
            telephone = extract.telephone(content_node)
            website = extract.website(content_node)
            consulates = extract.consulate_cities(content_node)

            count = count + 1
            data.append({"item_count": count,
                         "group_index": group_index,
                         "div_id": div_id,
                         "accordion_title": accordion_title,
                         "first_h3": first_h3,
                         "first_h2": first_h2,
                         "hosts_emb": hosts_emb,
                         "telephone": telephone,
                         "address": address,
                         "website": website,
                         "consulates": consulates

                         })

    # data = process.correct_some_country_titles(data)
    for datum in data:
        print("_________________________")
        print(datum)

    return data


def main() -> None:
    main_page = "https://www.ireland.ie/en/dfa/embassies/"
    html = get_html_tree_for(main_page)
    data = parse_landing_page(html)

    print(data)


if __name__ == '__main__':
    main()
