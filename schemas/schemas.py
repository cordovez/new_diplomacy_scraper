from typing import NamedTuple


class DiplomatName(NamedTuple):
    """
    Represents a named tuple for storing a diplomat's first and last name. This is
    used by the Diplomat model to split the full name.
    """
    first: str
    last: str
