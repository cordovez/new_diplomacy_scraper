import json
import time
from rich import print
import os
from parsers import parse
from scrapers import scrape


def _save_to_json(data: list[dict]) -> None:
    with open("data/scrape_results.json", "w") as file:
        json.dump(data, file, indent=4)


def scrape_dfa() -> None:
    """
    To scrape from scratch, delete or rename "data/scraped.html", at a cost of
    around 200 credits, otherwise, it is reading html from file
    """
    html = scrape.scrape_or_read_from_file()
    data = parse.landing_page(html)
    _save_to_json(data)


def main() -> None:
    pass


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:2f} seconds")
