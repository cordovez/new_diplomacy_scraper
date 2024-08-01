import beanie
from mongodb.db import init_db
from mongodb.models import models
from mongodb.models.models import ContactDetails
from services.normalise_countries import (correct_accredited_countries,
                                          correct_dublin_missions,
                                          correct_london_missions, correct_cc_countries)
from services import do_string


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

def _assign_country_code_to_country(country_name: str) -> str:
    """assign an ISO country code to country name"""
    country_dicts = correct_cc_countries()
    for country in country_dicts:
        # if country_name == "Slovakia":
        #     country_name = "Slovak Republic"
        if country["name"] == country_name:
            return country["alpha-3"]


def _country_accredited_to_ie(country: str) -> bool:
    """Countries which have been accredited to Ireland"""
    lower_case_country = country.lower()
    accredited_countries = correct_accredited_countries()

    return lower_case_country in accredited_countries


def _location_of_foreign_mission_for(country: str) -> str | None:
    """ Countries which have been accredited to Ireland, will have a mission in either
    London or Dublin.
    """
    dublin_missions = [(country, "dublin") for country in correct_dublin_missions()]
    london_missions = [(country, "london") for country in correct_london_missions()]

    foreign_missions = dublin_missions + london_missions

    if country is None:
        return None
    for mission in foreign_missions:
        if country.lower() in mission[0]:
            return mission[1]


def _is_a_special_mission(country: str) -> bool:
    inner_special_missions = ["Palestinian", "Partnership",
                              "Permanent Representation",
                              "Permanent Mission"]

    if any(term.lower() in country.lower() for term in inner_special_missions):
        return True


def _clean_address(address: str) -> str | None:
    return address.replace(
        " \n                    \n                    \n                      ",
        ";").replace("\n", "").strip()


# ------------------------------------------------------------------------------
# Main Parsers
# ------------------------------------------------------------------------------

special_missions = ["Palestinian", "Partnership",
                    "Permanent Representation",
                    "Permanent Mission"]


async def countries_from_json(json_data: dict) -> list[beanie.Document]:
    # sourcery skip: remove-unnecessary-cast
    """Country information, for all countries listed on the DFA website. JSON data
    includes some special missions, which are excluded here."""

    objects = []

    for item in json_data:
        title = item["accordion_title"]
        if (not any(term.lower() in title.lower() for term in special_missions) and item
                not in objects):
            objects.append(item)

    await init_db()
    return [
        models.Country(
            country_name=item["accordion_title"],
            accredited_to_ireland=_country_accredited_to_ie(item["accordion_title"]),
            with_mission_in=_location_of_foreign_mission_for(item["div_id"]),
            hosts_irish_mission=bool(item["embassy_url"] != "none found"),
            iso3_code=_assign_country_code_to_country(item["accordion_title"]),
            )
        for item in objects
        ]


async def special_missions_from_json(json_data: dict) -> list[beanie.Document]:
    objects = []
    for item in json_data:
        item["address"] = _clean_address(item["address"])
        if _is_a_special_mission(item["accordion_title"]):
            objects.append(item)

    return [models.Representation(
        head_of_mission=models.Diplomat(first_name=mission["head_of_mission"],
                                        last_name=mission["head_of_mission"],
                                        mission_title=mission["accordion_title"],
                                        mission_type="ambassador unless "),
        contact=models.ContactDetails(
            address1=mission["address"],
            city=mission["address"],
            tel=mission["telephone"],
            ),
        website=mission["embassy_url"],
        representation_name=mission["accordion_title"],
        host_city=mission["address"],
        host_country=mission["address"],
        ) for mission in objects]


async def consulates_from_json(json_data: dict) -> list[beanie.Document]:
    objects = []
    for item in json_data:
        if len(item["consulates"]) > 0:
            objects.extend(iter(item["consulates"]))

    return [models.Consulate(
        host_city=item["city"],
        head_of_mission=models.Diplomat(
            first_name=do_string.name_splitting_from(item["consul_general"]).first,
            last_name=do_string.name_splitting_from(item["consul_general"]).last,
            mission_title="consulate",
            mission_type="consulate"
            ),
        consulate_url=item["consulate_url"]) for item in objects]


def get_consulates(consulates: list[dict]) -> list[beanie.Document]:
    return [models.Consulate(
        host_city=item["city"],
        head_of_mission=models.Diplomat(
            first_name=do_string.name_splitting_from(item["consul_general"]).first,
            last_name=do_string.name_splitting_from(item["consul_general"]).last,
            mission_title="consulate",
            mission_type="consulate"
            ),
        consulate_url=item["consulate_url"]) for item in consulates]


def _is_embassy(item: dict) -> bool:
    country_in_url = do_string.country_extraction_from(item["embassy_url"])
    country = item["accordion_title"]

    if (not _is_a_special_mission(country)
            and country_in_url == country.lower()):
        return True


def embassies_from_json(json_data: dict) -> list[beanie.Document]:
    objects = []
    for item in json_data:
        if _is_embassy(item):
            item["address"] = _clean_address(item["address"])
            objects.append(item)

    return [models.Embassy(
        host_country=item["accordion_title"],
        head_of_mission=models.Diplomat(
            first_name=do_string.name_splitting_from(item["head_of_mission"]).first,
            last_name=do_string.name_splitting_from(item["head_of_mission"]).last,
            mission_title=f"Embassy of Ireland {item['accordion_title']}"
            if item["embassy_url"] != "none "
                                                                              "found"
            else
            "",
            mission_type="embassy"
            ),
        contact=ContactDetails(),
        website=item["embassy_url"],
        consulates=get_consulates(item["consulates"])) for item in objects

        ]
