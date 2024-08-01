import json
import time
from rich import print
from parsers import parse
from scrapers import scrape
import asyncio
from mongodb.db import init_db
from services import process
from services import merge_json
from scrapers.scrape import scrape_or_read_from_file
from scrapers.addresses import get_html
from services.merge_json import head_of_mission

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
    with open("data/scrape_updated.json", "r") as file:
        return json.load(file)


json_data = read_scraped_json()


async def main() -> None:
    await init_db()
    # To Scrape, uncomment the following function (208 credits)
    # scrape_dfa()
    # countries = await process.countries_from_json(json_data)
    # special_missions = await process.special_missions_from_json(json_data)
    # consulates = await process.consulates_from_json(json_data)
    embassies =  process.embassies_from_json(json_data)
    print(list(emb.host_country for emb in embassies))
    #


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:2f} seconds")
