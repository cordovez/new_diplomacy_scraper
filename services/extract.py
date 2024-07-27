import re
import httpx
from selectolax.parser import Node
from scrapers.scraper import get_html_tree_for

# -----------------------------------------------------
# Direct call functions
# -----------------------------------------------------


def telephone(content_node: Node) -> str:
    telephone_node = content_node.css_first('a[aria-label="Telephone"]')
    tel = telephone_node.text(strip=True) if telephone_node else "None"
    return tel.replace("Tel:", "")


def address(content_node: Node) -> str:
    found_address = content_node.css_first("address").text(strip=True) if (
        content_node.css_first(
        "address")) else "None"
    return re.sub(r'\s*\n\s*', '\n ', found_address)


def embassy_url(content_node: Node) -> str:
    """
    Not implemented yet
    """
    a_tags = content_node.css("a")

    for a_tag in a_tags:
        b_tag = a_tag.css_first("b")
        if b_tag and b_tag.text(strip=True) == "Embassy Website":
            return a_tag.attributes.get("href", "No href found")

    return "none found"


def consulates(node: Node):
    a_links = node.css("ul li a")
    data = []
    cities = [link.text().replace("Consulate General of Ireland, ", "")
              for link in a_links if "Consulate General of Ireland" in
              link.text()]
    for city in cities:
        url = _consulate_url(node, city)
        consul_general = head_of_mission(url)
        data.append({"city": city, "consulate_url": url,
                     "consul_general": consul_general})

    return data


def presence_status(node: Node) -> bool:
    if text_block := node.css_first("div.rich_text__summary"):
        if first_paragraph := text_block.css_first("p"):
            response = first_paragraph.text(strip=True)
            return "We do not have an Embassy in this country" in response
        else:
            return "none found"


def h2(node: Node) -> str:
    return node.css_first("h2").text() if node.css_first("h2") else "none found"


# TODO: change 'Embassy of Ireland, Washington' to 'Embassy of Ireland, United States
#  ... for all items'
def h3(node: Node) -> str:
    return node.css_first("h3").text() if (
                node.css_first("h3")) else "none found"


# -----------------------------------------------------
# helper functions
# -----------------------------------------------------

def _consulate_url(node: Node, city: str) -> str:
    collapsed_city = city.lower().replace(" ", "")
    city_node = node.css_first(f"div#{collapsed_city}")

    all_a_tags = city_node.css("a")
    for a_tag in all_a_tags:
        b_tag = a_tag.css_first("b")
        if b_tag and b_tag.text(strip=True) == "Consulate Website":
            return a_tag.attributes.get("href", "No href found")

    return "none found"


def head_of_mission(url: str):
    if url == "none found":
        return "none found"

    try:
        if not url.startswith("https://www.ireland.ie"):
            url = f"https://www.ireland.ie{url}"

        html = get_html_tree_for(url)

        if diplomat := html.css_first("div.block-person h3"):
            return diplomat.text(strip=True)

        return "none found"

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} for URL: {e.request.url}")
        return "none found"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "none found"
