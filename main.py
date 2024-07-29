import json
import time
from rich import print
from parsers import parse
from scrapers import scrape
import asyncio
from services.normalise_countries import difference_from_two_lists, correct_accredited_countries
from services.process import parse_country_items


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


def read_scraped_json():
    with open("data/scrape_results.json", "r") as file:
        return json.load(file)

json_data = read_scraped_json()


async def main() -> None:
    await parse_country_items(json_data)
    # print(correct_accredited_countries())
    # print(difference_from_two_lists())

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:2f} seconds")
