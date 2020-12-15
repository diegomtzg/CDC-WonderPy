from enum import Enum

class CDCWonderExceptions(Enum):
    """
    Strings describing different known issues that can be statically checked
    when using the API.
    """
    race_exception = "Race has both 'All' and other options selected. Please select either 'All' or specific options."
    hispanic_origin_all_exception = "Hispanic Origin has both 'All' and other options selected. Please select either 'All' or specific options."
    hispanic_origin_ns_exception = "The 'Not Stated' Hispanic Origin value cannot be combined with other values."
    autopsy_exception = "Autopsy has both 'All' and other options selected. Please select either 'All' or specific options."
    gender_exception = "Gender has both 'All Genders' and other options selected. Please select either 'All' or specific options."
    place_of_death_exception = "PlaceOfDeath has both 'All' and other options selected. Please select either 'All' or specific options."
    weekday_exception = "PlaceOfDeath has both 'All' and other options selected. Please select either 'All' or specific options."
