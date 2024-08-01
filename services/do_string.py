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
    parts = url_path.strip('/').split('/')

    # Check if the URL path has at least 3 parts
    if len(parts) >= 2:
        return parts[1]  # The country name is the second part
    else:
        return "Invalid URL path"