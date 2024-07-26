def determine_if_represented(label: str, title: str) -> bool:
    """
    Corrects two mis-matched labels and titles, and returns True or False
    if item title and item labels are match.
    """
    match label:
        case "Netherlands":
            label = "The Netherlands"
        case "Russian Federation":
            label = "Russia"
        case _:
            label = label

    return title.replace("Embassy of Ireland, ", "") == label


def correct_some_country_titles(data: list[dict]) -> list[dict]:
    """
    The titles of five countries are normalised.
    """
    missing_names = ["Luxembourg", "Malawi", "Namibia", "Zambia", "Philippines"]
    for item in data:
        if item.get("label") in missing_names:
            item["title"] = f"Embassy of Ireland, {item['label']}"

    for item in data:
        if item.get("title") == "Embassy of Ireland, UAE":
            item["title"] = f"Embassy of Ireland, United Arab Emirates"

    for item in data:
        item["is_represented"] = determine_if_represented(item["label"], item["title"])
    return data
