from services import extract
from selectolax.parser import HTMLParser


# -------------------------------------------------
# parsers
# -------------------------------------------------
def landing_page(html_tree: HTMLParser) -> list[dict]:
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
            address: str = extract.address(content_node)
            telephone: str = extract.telephone(content_node)
            embassy_url: str = extract.embassy_url(content_node)
            consulates: list[dict] = extract.consulates(content_node)
            head_of_mission: str = extract.head_of_mission(embassy_url)

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
                         "embassy_url": embassy_url,
                         "consulates": consulates,
                         "head_of_mission": head_of_mission
                         })
    print(f"processing accordion {count}")
    return data
