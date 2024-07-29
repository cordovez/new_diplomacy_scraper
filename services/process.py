from rich import print
from mongodb.db import init_db
from mongodb.models import models
from services.normalise_countries import (correct_accredited_countries,
                                          correct_dublin_missions,
                                          correct_london_missions, correct_cc_countries)


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
            item["accordion_title"] = "Embassy of Ireland, United Arab Emirates"

    # for item in data:
    #     item["is_represented"] = determine_if_represented(item["div_id"], 
    #     item["accordion_title"])
    return data


# ------------------------------------------------------------------------------
# Main Functions
# ------------------------------------------------------------------------------


async def save_countries_to_db():
    countries = _countries_from_json(RAW_DATA)
    return await into_db.save_many_to_collection(CountryDocument, countries)


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

def _assign_country_code_to_embassy(country_name: str) -> str:
    country_dicts = correct_cc_countries()

    for country in country_dicts:
        # if country_name == "Slovakia":
        #     country_name = "Slovak Republic"
        if country["name"] == country_name:
            return country["alpha-3"]


def _country_accredited_to_ie(country: str) -> bool:
    lower_case_country = country.lower()
    accredited_countries = correct_accredited_countries()

    return lower_case_country in accredited_countries


def _location_of_foreign_mission_for(country: str) -> str | None:
    """ Countries which have been accredited to Ireland, may have a mission in either
    London or Dublin
    """
    dublin_missions = [(country, "dublin") for country in correct_dublin_missions()]
    london_missions = [(country, "london") for country in correct_london_missions()]

    foreign_missions = dublin_missions + london_missions
    # country = _regularise_country_name(country)
    #
    if country is None:
        return None
    for mission in foreign_missions:
        if country.lower() in mission[0]:
            return mission[1]


async def parse_country_items(json_data: dict) -> None:
    objects = []
    others = []
    terms_to_avoid = ["Palestinian", "Partnership", "Permanent Representation",
                      "Permanent Mission"]

    for item in json_data:
        title = item["accordion_title"]
        if not any(term.lower() in title.lower() for term in terms_to_avoid):
            if item not in objects:
                objects.append(item)

    await init_db()
    countries = [
        models.Country(
            country_name=item["accordion_title"],
            accredited_to_ireland=_country_accredited_to_ie(item["accordion_title"]),
            with_mission_in=_location_of_foreign_mission_for(item["div_id"]),
            hosts_irish_mission=bool(item["embassy_url"] != "none found"),
            iso3_code=_assign_country_code_to_embassy(item["accordion_title"]),
            )
        for item in objects
        ]

    # some_countries_incorrect = [country.country_name for country in countries if
    #                             country.iso3_code is None]

    print(countries)
    # names = [country.country_name for country in others ]
    # print(len(countries))
    # print(some_countries_incorrect)
