from schemas.schemas import DiplomatName
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



