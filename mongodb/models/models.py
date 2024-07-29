import beanie
from typing import Literal, Optional

class Country(beanie.Document):
    country_name: str
    accredited_to_ireland: Optional[bool] | None = None
    with_mission_in: Optional[Literal["dublin", "london"]] | None = None
    hosts_irish_mission: Optional[bool] | None = None
    iso3_code: Optional[str] | None = None


class Mission(beanie.Document):
    contact: dict
    website: str
    type_of: str
    title: str
    host_city: str
    host_country: str
    head_of_mission: str
    consulates: list

class Diplomat(beanie.Document):
    first_name: str
    last_name: str
    mission_title: str
    mission_type: str
