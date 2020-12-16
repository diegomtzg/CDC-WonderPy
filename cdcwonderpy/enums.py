from enum import Enum

#########################################
#### Grouping Enums
#########################################
class Grouping(Enum):
    # Demographics
    TEN_YEAR_AGE_GROUPS = "D76.V5"
    FIVE_YEAR_AGE_GROUPS = "D76.V51"
    SINGLE_YEAR_AGE_GROUPS = "D76.V52"

    GENDER = "D76.V7"
    HISPANIC_ORIGIN = "D76.V17"
    RACE = "D76.V8"

    # Year and Month
    YEAR = "D76.V1-level1"
    MONTH = "D76.V1-level2"

    # Weekday, Autopsy, Place of Death
    WEEKDAY = "D76.V24"
    AUTOPSY = "D76.V20"
    PLACE_OF_DEATH = "D76.V21"

    # Cause single Death
    LEADING_CAUSES_OF_DEATH = "D76.V28"
    ICD_CHAPTER = "D76.V2-level1"
    ICD_SUBCHAPTER = "D76.V2-level2"
    CAUSE_OF_DEATH = "D76.V2-level3"
    ICD10_CAUSE_LIST_113 = "D76.V4"
    INJURY_INTENT = "D76.V22"
    INJURY_MECHANISM_AND_ALL_OTHER_LEADING_CAUSES = "D76.V23"
    DRUG_OR_ALCOHOL_INDUCED_CAUSES = "D76.V25"

#########################################
#### Demographic Enums
#########################################
class Gender(Enum):
    ALL = "*All*"
    MALE = "M"
    FEMALE = "F"

class HispanicOrigin(Enum):
    ALL = "*All*"
    HISPANIC_OR_LATINO = "2135-2"
    NOT_HISPANIC_OR_LATINO = "2186-2"
    NOT_STATED = "NS"

class Race(Enum):
    ALL = "*All*"
    AMERICAN_INDIAN_OR_ALASKAN_NATIVE = "1002-5"
    ASIAN_OR_PACIFIC_ISLANDER = "A-PI"
    BLACK_OR_AFRICAN_AMERICAN = "2054-5"
    WHITE = "2106-3"

#########################################
#### Chronology Enums
#########################################
class Weekday(Enum):
    ALL = "*All*"
    SUN = "1"
    MON = "2"
    TUE = "3"
    WED = "4"
    THU = "5"
    FRI = "6"
    SAT = "7"
    UNKNOWN = "9"

#########################################
#### Miscellaneous Enums
#########################################
class PlaceOfDeath(Enum):
    ALL = "*All*"
    MEDICAL_FACILITY_INPATIENT = "1"
    MEDICAL_FACILITY_OUTPATIENT = "2"
    MEDICAL_FACILITY_DEAD_ON_ARRIVAL = "3"
    MEDICAL_FACILITY_UNKNOWN_STATUS = "10"
    DECEDENT_HOME = "4"
    HOSPICE_FACILITY = "5"
    NURSING_HOME = "6"
    OTHER = "7"
    UNKNOWN = "9"

class Autopsy(Enum):
    ALL = "*All*"
    NO = "N"
    YES = "Y"
    UNKNOWN = "U"
