

class Country:
    country_name: str
    accredited_to_ireland: bool
    with_mission_in: "dublin" | "london"
    hosts_irish_mission: bool
    iso3_code: str


class Mission:
    contact: dict
    website: str
    type_of: str
    title: str
    host_city: str
    host_country: str
    head_of_mission: str
    consulates: list

class Diplomat:
    first_name: str
    last_name: str
    mission_title: str
    mission_type: str
