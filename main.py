import json
import time
from rich import print
from scraper_parsers import parse
from scrapers import scrape
import asyncio
from mongodb.db import init_db
from services import process
from mongodb.query import into_db
from mongodb.models import models

# ------------------Main scraper functions
def _save_to_json(data: list[dict]) -> None:
    """
    Saves the provided data to a JSON file with an indent of 4 spaces.
    """
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


# ------------------Once scraped, this reads the json file

def read_scraped_json():
    """
    Saves the provided data to a JSON file with an indent of 4 spaces.
    """
    with open("data/scrape_updated.json", "r") as file:
        return json.load(file)


# ------------------This is the data passed to each processor below
json_data = read_scraped_json()


async def main() -> None:
    await init_db()
    # ------------------To Scrape, uncomment the following function (208 credits)
    # scrape_dfa()

    # ------------------To convert data into beanie.Document models:
    # countries = process.countries_from_json(json_data)
    special_missions = process.special_missions_from_json(json_data)
    # consulates = process.consulates_from_json(json_data)
    # embassies = process.embassies_from_json(json_data)
    # diplomats = process.diplomats_from_json(json_data)
    # print(diplomats)
    # print([diplomat for diplomat in diplomats if diplomat.last_name == 'Almqvist'])

    # -----------------To Save documents to MongoDB
    result = await into_db.save_many_to_collection(models.Representation, special_missions)
    print(result)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:2f} seconds")
