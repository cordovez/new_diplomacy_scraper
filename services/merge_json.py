import json


def head_of_mission(scrape_file: str, backup_file: str, output_file: str):
    """
    Merges head of mission and consulate information from a backup JSON file into a
    scrape JSON file.

    Args:
        scrape_file: The path to the JSON file with scraped data.
        backup_file: The path to the JSON file with backup data.
        output_file: The path to save the merged JSON data.

    Returns:
        None
    """
    with open(scrape_file, 'r', encoding='utf-8') as f:
        scrape_data = json.load(f)

    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)

    for scrape_item, backup_item in zip(scrape_data, backup_data):
        if scrape_item.get("head_of_mission") in (None, "none found"):
            scrape_item["head_of_mission"] = backup_item.get("head_of_mission", "")

    for scrape_item, backup_item in zip(scrape_data, backup_data):
        if len(scrape_item["consulates"]) > 0:
            scrape_item["consulates"] = backup_item["consulates"]

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(scrape_data, f, indent=4, ensure_ascii=False)

# if __name__ == '__main__':
# scrape_file = 'data/scrape_results.json'
# backup_file = 'data/scrape_results_backup.json'
# output_file = 'data/scrape_updated.json'
#
# head_of_mission(scrape_file, backup_file, output_file)
