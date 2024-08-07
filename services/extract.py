import httpx
from selectolax.parser import Node
from scrapers import scrape


# -----------------------------------------------------
# Direct call functions
# -----------------------------------------------------


def telephone(content_node: Node) -> str:
    telephone_node = content_node.css_first('a[aria-label="Telephone"]')
    tel = telephone_node.text(strip=True) if telephone_node else "None"
    return tel.replace("Tel:", "")


def address(content_node: Node) -> str:
    return content_node.css_first("address").text() if (
        content_node.css_first("address")) else "none found"


def embassy_url(content_node: Node) -> str:
    """
    Extracts the URL of the embassy website from a Node object.

    Args:
        content_node: The Node object containing the embassy information.

    Returns:
        A string representing the URL of the embassy website or "none found" if not
        available.
    """
    a_tags = content_node.css("a")

    for a_tag in a_tags:
        b_tag = a_tag.css_first("b")
        if b_tag and b_tag.text(strip=True) == "Embassy Website":
            return a_tag.attributes.get("href", "No href found")

    return "none found"


def consulates(node: Node):
    """
    Extracts information about consulates from a Node object.

    Args:
        node: The Node object containing consulate information.

    Returns:
        A list of dictionaries with details about consulates including city, consulate
        URL, and consul general.
    """
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
    """
    Checks the presence of an Irish embassy in a foreign country based on the content 
    of a Node.

    Args:
        node: The Node object to check for presence status.

    Returns:
        A boolean indicating the presence status based on the content of the Node.
    """
    if text_block := node.css_first("div.rich_text__summary"):
        if first_paragraph := text_block.css_first("p"):
            response = first_paragraph.text(strip=True)
            return "We do not have an Embassy in this country" in response
        else:
            return False


def h2(node: Node) -> str:
    return node.css_first("h2").text() if node.css_first("h2") else "none found"


def h3(node: Node) -> str:
    return node.css_first("h3").text() if (
        node.css_first("h3")) else "none found"


def head_of_mission(url: str):
    """
    Extracts the name of the head of mission from a given URL.

    Args:
        url: The URL to extract the head of mission's name from.

    Returns:
        A string representing the name of the head of mission or "none found" if not 
        available.
    """
    if url == "none found":
        return "none found"

    try:
        if not url.startswith("https://www.ireland.ie"):
            url = f"https://www.ireland.ie{url}"

        html = scrape.scrape_html_tree_for(url)

        if diplomat := html.css_first("div.block-person h3"):
            return diplomat.text(strip=True)

        return "none found"

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} for URL: {e.request.url}")
        return "none found"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "none found"


# -----------------------------------------------------
# helper functions
# -----------------------------------------------------


def _consulate_url(node: Node, city: str) -> str:
    """
    Extracts the consulate website URL from a specific city node.

    Args:
        node: The Node object representing the city node.
        city: The name of the city to extract the consulate URL from.

    Returns:
        A string representing the consulate website URL or "none found" if not found.
    """
    collapsed_city = city.lower().replace(" ", "")
    city_node = node.css_first(f"div#{collapsed_city}")

    all_a_tags = city_node.css("a")
    for a_tag in all_a_tags:
        b_tag = a_tag.css_first("b")
        if b_tag and b_tag.text(strip=True) == "Consulate Website":
            return a_tag.attributes.get("href", "No href found")

    return "none found"
