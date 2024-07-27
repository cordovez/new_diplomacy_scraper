def determine_if_represented(div_id: str, title: str) -> bool:
    """
    Corrects two mis-matched labels and titles, and returns True or False
    if item title and item labels are match.
    """
    match div_id:
        case "Netherlands":
            div_id = "The Netherlands"
        case "Russian Federation":
            div_id = "Russia"
        case _:
            div_id = div_id

    return title.replace("Embassy of Ireland, ", "") == div_id


def correct_some_country_titles(data: list[dict]) -> list[dict]:
    """
    The titles of five countries are normalised.
    """
    missing_names = ["Luxembourg", "Malawi", "Namibia", "Zambia", "Philippines"]
    for item in data:
        if item.get("div_id") in missing_names:
            item["accordion_title"] = f"Embassy of Ireland, {item['div_id']}"

    for item in data:
        if item.get("accordion_title") == "Embassy of Ireland, UAE":
            item["accordion_title"] = f"Embassy of Ireland, United Arab Emirates"

    # for item in data:
    #     item["is_represented"] = determine_if_represented(item["div_id"], item["accordion_title"])
    return data
