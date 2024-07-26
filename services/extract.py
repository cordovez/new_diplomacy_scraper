import re

from selectolax.parser import Node


def telephone(content_node: Node) -> str:
    telephone_node = content_node.css_first('a[aria-label="Telephone"]')
    telephone = telephone_node.text() if telephone_node else "None"
    return telephone.replace("Tel:", "").strip()


def address(content_node: Node) -> str:
    address = content_node.css_first("address").text() if content_node.css_first(
        "address") else "None"

    cleaned_address = re.sub(r'\s*\n\s*', '\n', address.strip())

    return cleaned_address


def title(content_node: Node) -> str:
    embassy_title = content_node.css_first("h3").text() if content_node.css_first("h3") \
        else "None"
    return embassy_title.strip()


def website(content_node: Node) -> str:
    """
    Not implemented yet
    """
    return ""
    # p_node = content_node.css_first("p[data-block-key='ncby3']")
    # if p_node is not None:
    #     a_tag = p_node.css_first("a[href]")
    #     if a_tag is not None:
    #         return a_tag.attributes.get('href', 'None')


def consulates(nodes: list[Node]):
    return [node.text().replace("Consulate General of Ireland, ", "")
            for node in nodes if "Consulate General of Ireland" in node.text()]
