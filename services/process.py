import beanie
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
    """
    The words in the 'inner_special_missions' appear in the title of the mission
    """
    inner_special_missions = ["Palestinian", "Partnership",
                              "Permanent Representation",
                              "Permanent Mission"]

    if any(term.lower() in country.lower() for term in inner_special_missions):
        return True


def _clean_address(address: str) -> str | None:
    return address.replace(
        " \n                    \n                    \n                      ",
        ";").replace("\n", "").strip()


def _is_ie_embassy_present(item: dict) -> bool:
    if item["embassy_url"] != "none found":
        country_in_url = do_string.country_extraction_from(item["embassy_url"])
        country = item["accordion_title"]

        if (not _is_a_special_mission(country)
                and country_in_url == country.lower()):
            return True

    return False


def _who_covers_this_country(item: dict) -> str:
    """
    Determines the embassy covering a country based on the provided item's data.

    Args:
        item: A dictionary containing information about the country and embassy.

    Returns:
        A string representing the entity covering the country or None if not found.
    """
    if item["embassy_url"] != "none found":
        country_in_url = do_string.country_extraction_from(item["embassy_url"])
        country = item["accordion_title"]

        if country_in_url != country.lower():
            return item["first_h3"].replace("Embassy of Ireland,", "").strip()


# ------------------------------------------------------------------------------
# Main Parsers
# ------------------------------------------------------------------------------

special_missions = ["Palestinian", "Partnership",
                    "Permanent Representation",
                    "Permanent Mission"]


def diplomats_from_json(json_data: dict) -> list[beanie.Document]:
    """ All names found in JSON"""
    diplomats = []
    seen_diplomats = set()
    for item in json_data:
        ambassador = item["head_of_mission"]

        if ambassador != "none found" and ambassador not in seen_diplomats:
            seen_diplomats.add(ambassador)
            diplomats.append({
                "full_name": ambassador,
                "mission_title": item["first_h3"],
                "mission_type": "embassy",
                "mission": item["accordion_title"],
                })

    for item in json_data:
        if len(item["consulates"]) > 0:
            for consulate in item["consulates"]:
                consul = consulate["consul_general"]
                diplomats.append({
                    "full_name": consul,
                    "mission_title": f"Consulate General of Ireland, "
                                     f"{consulate['city']}",
                    "mission_type": "consulate",
                    "mission": consulate["city"],
                    })
    return [models.Diplomat(
        full_name=diplomat["full_name"],
        first_name=do_string.name_splitting_from(diplomat["full_name"]).first,
        last_name=do_string.name_splitting_from(diplomat["full_name"]).last,
        mission_title=diplomat["mission_title"],
        mission_type=diplomat["mission_type"],
        mission=diplomat["mission"]
        ) for diplomat in diplomats]


def countries_from_json(json_data: dict) -> list[beanie.Document]:
    # sourcery skip: remove-unnecessary-cast
    """Country information, for all countries listed on the DFA website. JSON data
    includes some special missions, which are excluded here."""

    # objects = []

    for item in json_data:
        if not _is_a_special_mission(item["accordion_title"]):
            return [
                models.Country(
                    country_name=item["accordion_title"],
                    accredited_to_ireland=_country_accredited_to_ie(
                        item["accordion_title"]),
                    with_mission_in=_location_of_foreign_mission_for(item["div_id"]),
                    hosts_irish_mission=_is_ie_embassy_present(item),
                    iso3_code=_assign_country_code_to_country(item["accordion_title"]),
                    is_covered_by=_who_covers_this_country(item)
                    )
                for item in json_data
                ]


def special_missions_from_json(json_data: dict) -> list[beanie.Document]:
    """
    Extracts and processes special mission data from a JSON dictionary.

    Args:
        json_data: A dictionary containing data about special missions.

    Returns:
        A list of Beanie Document objects representing the processed special mission data.
    """
    objects = []
    for item in json_data:
        if _is_a_special_mission(item["accordion_title"]):
            item["address"] = _clean_address(item["address"])
            objects.append(item)

    return [models.Representation(
        head_of_mission=models.Diplomat(
            full_name=mission["head_of_mission"],
            first_name=do_string.name_splitting_from(mission["head_of_mission"]).first,
            last_name=do_string.name_splitting_from(mission["head_of_mission"]).last,
            mission_title=mission["accordion_title"],
            mission_type="representation"
            ),
        contact=models.ContactDetails(
            address1=mission["address"],
            tel=mission["telephone"].strip(),
            ),
        website=mission["embassy_url"],
        representation_name=mission["accordion_title"],
        host_city=do_string.extract_city_and_country_from(mission["address"]).city,
        host_country=do_string.extract_city_and_country_from(mission["address"]).country,
        ) for mission in objects]


def consulates_from_json(json_data: dict) -> list[beanie.Document]:
    """
    Extracts consulate data from a JSON dictionary and processes it.

    Args:
        json_data: A dictionary containing data about consulates.

    Returns:
        A list of Beanie Document objects representing the processed consulate data.
    """
    objects = []
    for item in json_data:
        if len(item["consulates"]) > 0:
            objects.extend(iter(item["consulates"]))

    return get_consulates(objects)


def get_consulates(consulates: list[dict]) -> list[beanie.Document]:
    """
    Processes a list of consulate data dictionaries into Beanie Document objects.

    Args:
        consulates: A list of dictionaries containing consulate data.

    Returns:
        A list of Beanie Document objects representing the processed consulate data.
    """
    return [models.Consulate(
        host_city=item["city"],
        head_of_mission=models.Diplomat(
            full_name=item["consul_general"],
            first_name=do_string.name_splitting_from(item["consul_general"]).first,
            last_name=do_string.name_splitting_from(item["consul_general"]).last,
            mission_title=f"Consulate General of Ireland, {item['city']}",
            mission_type="consulate"
            ),
        consulate_url=item["consulate_url"]) for item in consulates]


def embassies_from_json(json_data: dict) -> list[beanie.Document]:
    """
    Processes embassy data from a JSON dictionary into Beanie Document objects.

    Args:
        json_data: A dictionary containing data about embassies.

    Returns:
        A list of Beanie Document objects representing the processed embassy data.
    """
    objects = []
    for item in json_data:
        if _is_ie_embassy_present(item):
            item["address"] = _clean_address(item["address"])
            objects.append(item)

    return [models.Embassy(
        host_country=item["accordion_title"],
        head_of_mission=models.Diplomat(
            full_name=item["head_of_mission"],
            first_name=do_string.name_splitting_from(item["head_of_mission"]).first,
            last_name=do_string.name_splitting_from(item["head_of_mission"]).last,
            mission_title=f"Embassy of Ireland, {item['accordion_title']}",
            mission_type="embassy"
            ),
        contact=ContactDetails(address1=item["address"], tel=item["telephone"]),
        website=item["embassy_url"],
        consulates=get_consulates(item["consulates"])) for item in objects

        ]
