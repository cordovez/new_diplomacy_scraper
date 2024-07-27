import httpx
from selectolax.parser import HTMLParser
from rich import print
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

from services import extract
from services.extract import presence_status

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_proxy_url(url):
    payload = {"api_key": API_KEY, "url": url}
    return f"https://proxy.scrapeops.io/v1/?{urlencode(payload)}"


def get_html(client: httpx.Client, url: str) -> HTMLParser:
    response = client.get(url, timeout=None)
    response.raise_for_status()
    return HTMLParser(response.text)


def parse_landing_page(html_tree: HTMLParser):
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

    return None

def main():
    url = "https://www.ireland.ie/en/dfa/embassies/"
    proxy_url = get_proxy_url(url)

    with httpx.Client() as client:
        client.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X "
                          "10_15_7) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/119.0.0.0 "
                          "Safari/537.36"})
        tree = get_html(client, proxy_url)

    data = parse_landing_page(tree)
    # accordions = parse_accordions(html)
    # data = parse_data(accordions)
    print(data)

    # results = []

    # response = requests.get(
    #     url='https://proxy.scrapeops.io/v1/',
    #     params={
    #         'api_key': '87ddbbdf-3f21-4adb-8027-d10b9881a704',
    #         'url': 'https://www.ireland.ie/en/dfa/embassies/',
    #         },
    #     )
    #


# def parse_detail_page(html: HTMLParser) -> dict:
#     element_list = html.css("script[type='application/ld+json']")
#     for element in element_list:
#         data = json.loads(element.text())
#
#         for item in data:
#             if "offers" in item:
#                 yield item["offers"]


if __name__ == '__main__':
    main()
