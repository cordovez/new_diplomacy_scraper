import httpx
from selectolax.parser import HTMLParser, Node
from rich import print
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

from services import extract
from services import process

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_proxy_url(url):
    payload = {"api_key": API_KEY, "url": url}
    return f"https://proxy.scrapeops.io/v1/?{urlencode(payload)}"


def get_html(client: httpx.Client, url: str) -> HTMLParser:
    response = client.get(url, timeout=None)
    response.raise_for_status()
    html = HTMLParser(response.text)
    return html


def parse_landing_page(html_tree: HTMLParser):
    data = []
    for accordion in html_tree.css(".accordion"):
        label: str = accordion.attributes["id"]
        group_index: str = accordion.attributes["accordian"]  # the misspelling is in
        # html
        content_node = accordion.css_first(f"#answer-{group_index}")
        if content_node:
            title = extract.title(content_node)
            address = extract.address(content_node)
            telephone = extract.telephone(content_node)
            website = extract.website(content_node)
            is_represented = process.determine_if_represented(label, title)
            consulates = extract.consulates(content_node.css("ul li a")
)

            data.append({"label": label, "title": title, "telephone": telephone,
                         "address": address, "website": website,
                         "is_represented": is_represented, "consulates": consulates})

    data = process.correct_some_country_titles(data)

    # for i, datum in enumerate(data):

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
