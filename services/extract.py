import re

from selectolax.parser import Node


def telephone(content_node: Node) -> str:
    telephone_node = content_node.css_first('a[aria-label="Telephone"]')
    tel = telephone_node.text() if telephone_node else "None"
    return tel.replace("Tel:", "").strip()


def address(content_node: Node) -> str:
    found_address = content_node.css_first("address").text() if content_node.css_first(
        "address") else "None"
    return re.sub(r'\s*\n\s*', '\n', found_address.strip())


def website(content_node: Node) -> str:
    """
    Not implemented yet
    """
    a_tags = content_node.css("a")

    for a_tag in a_tags:
        b_tag = a_tag.css_first("b")
        if b_tag and b_tag.text(strip=True) == "Embassy Website":
            return a_tag.attributes.get("href", "No href found")

    return "No matching <a> tag found"


def consulate_cities(node: Node):
    a_links = node.css("ul li a")
    data = []
    cities = [link.text().replace("Consulate General of Ireland, ", "")
              for link in a_links if "Consulate General of Ireland" in
              link.text()]
    for city in cities:
        data.append({city: {"consulate_url": consulate_url(node, city)}})

    return data

def consulate_url(node: Node, city: str) -> str:
    collapsed_city = city.lower().replace(" ", "")
    city_node = node.css_first(f"div#{collapsed_city}")

    all_a_tags = city_node.css("a")
    for a_tag in all_a_tags:
        b_tag = a_tag.css_first("b")
        if b_tag and b_tag.text(strip=True) == "Consulate Website":
            return a_tag.attributes.get("href", "No href found")

    return "No matching <a> tag found"


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




