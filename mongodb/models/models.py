import beanie
from typing import Literal, Optional
# from mongodb.contact import ContactDetails
from beanie import UnionDoc
# from mongodb.diplomat import DiplomatDocument
import pydantic
import pymongo


class ContactDetails(pydantic.BaseModel):
    address1: Optional[str] | None = None
    address2: Optional[str] | None = None
    address3: Optional[str] | None = None
    address4: Optional[str] | None = None
    city: Optional[str] | None = None
    postal_code: Optional[str] | None = None
    region: Optional[str] | None = None
    country: Optional[str] | None = None
    tel: Optional[str] | None = None


class MissionUnion(UnionDoc):
    class Settings:
        name = "missions_union"
        class_id: "_class_id"  # noqa: F821


class Diplomat(beanie.Document):
    first_name: str
    last_name: str
    mission_title: str
    mission_type: str

    class Settings:
        name = "diplomats"
        indexes = [
            pymongo.IndexModel(
                keys=[("last_name", pymongo.ASCENDING)], name="last_name_ascend"
                ),
            pymongo.IndexModel(
                keys=[("last_name", pymongo.ASCENDING)],
                name="diplomat_last_ascend",
                ),
            ]


class Mission(beanie.Document):
    head_of_mission: Optional[Diplomat] | None = None
    contact: Optional[ContactDetails] | None = None
    website: Optional[str] | None = None


class Representation(Mission):
    type_of: str = "representation"
    representation_name: str
    host_city: str
    host_country: str

    class Settings:
        name = "representations"
        union_doc = MissionUnion
        indexes = [
            pymongo.IndexModel(
                keys=[("representation_name", pymongo.ASCENDING)],
                name="representation_ascend",
                ),
            ]


class Country(beanie.Document):
    country_name: str
    accredited_to_ireland: Optional[bool] | None = None
    with_mission_in: Optional[Literal["dublin", "london"]] | None = None
    hosts_irish_mission: Optional[bool] | None = None
    iso3_code: Optional[str] | None = None

    class Settings:
        name = "countries"
        indexes = [
            pymongo.IndexModel(
                keys=[("country_name", pymongo.ASCENDING)],
                name="country_name_ascending",
                ),
            ]


class Consulate(Mission):
    type_of: str = "consulate"
    host_city: str

    class Settings:
        name = "consulates"
        union_doc = MissionUnion
        indexes = [
            pymongo.IndexModel(
                keys=[("host_city", pymongo.ASCENDING)], name="consulate_city"
                ),
            ]


class Embassy(Mission):
    type_of: str = "embassy"
    host_country: str
    consulates: Optional[list[Consulate]] = []

    class Settings:
        name = "embassies"
        union_doc = MissionUnion
        indexes = [
            pymongo.IndexModel(
                keys=[("host_country", pymongo.ASCENDING)],
                name="embassy_ascending",
                ),
            ]
