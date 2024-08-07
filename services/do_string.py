from schemas.schemas import DiplomatName, CityCountry
import re


def name_splitting_from(fullname: str) -> DiplomatName:
    """
    Process a whole name string to extract the first and last name separately.
    """

    if not fullname:
        return DiplomatName("", "")

    match = re.match(r"(\S+)\s+(.+)", fullname)
    first, last = match.groups() if match else (fullname, "")
    return DiplomatName(first, last)


def country_extraction_from(url_path: str) -> str:
    """
    Extracts the country name from a URL path.

    Args:
        url_path: The URL path from which to extract the country name.

    Returns:
        A string representing the extracted country name or "Invalid URL path" if the path is invalid.
    """
    parts = url_path.strip('/').split('/')

    return "Invalid URL path" if len(parts) < 2 else parts[1]


def extract_city_and_country_from(address: str) -> CityCountry:
    pattern = r';\s*([\w\s-]+?)\s*;\s*([\w\s]+)\s*$'
    # pattern = r';\s*([a-zA-Z\s-]+?)\s*;\s*([a-zA-Z\s]+)\s*$'

    if match := re.search(pattern, address):
        city = match.group(1).strip()
        modified_city = re.sub(r'[0-9]+', '', city).strip()
        country = match.group(2).strip()
        return CityCountry(modified_city, country)
    else:
        return CityCountry(None, None)
