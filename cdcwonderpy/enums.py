from enum import Enum

#########################################
#### Grouping Enums
#########################################
class Grouping(Enum):
    # Demographics
    TenYearAgeGroups = "D76.V5"
    FiveYearAgeGroups = "D76.V51"
    SingleYearAgeGroups = "D76.V52"

    Gender = "D76.V7"
    HispanicOrigin = "D76.V17"
    Race = "D76.V8"

    # Year and Month
    Year = "D76.V1-level1"
    Month = "D76.V1-level2"

    # Weekday, Autopsy, Place single Death
    Weekday = "D76.V24"
    Autopsy = "D76.V20"
    PlaceOfDeath = "D76.V21"

    # Cause single Death
    LeadingCausesOfDeath = "D76.V28"
    ICDChapter = "D76.V2-level1"
    ICDSubChapter = "D76.V2-level2"
    CauseOfDeath = "D76.V2-level3"
    ICD10CauseList113 = "D76.V4"
    InjuryIntent = "D76.V22"
    InjuryMechanismAndAllOtherLeadingCauses = "D76.V23"
    DrugOrAlcoholInducedCauses = "D76.V25"

#########################################
#### Demographic Enums
#########################################
class Gender(Enum):
    All = "*All*"
    Male = "M"
    Female = "F"

class HispanicOrigin(Enum):
    All = "*All*"
    HispanicOrLatino = "2135-2"
    NotHispanicOrLatino = "2186-2"
    NotStated = "NS"

class Race(Enum):
    All = "*All*"
    AmericanIndianOrAlaskanNative = "1002-5"
    AsianOrPacificIslander = "A-PI"
    BlackOrAfricanAmerican = "2054-5"
    White = "2106-3"

#########################################
#### Chronology Enums
#########################################
class Weekday(Enum):
    All = "*All*"
    Sun = "1"
    Mon = "2"
    Tue = "3"
    Wed = "4"
    Thu = "5"
    Fri = "6"
    Sat = "7"
    Unknown = "9"

#########################################
#### Miscellaneous Enums
#########################################
class PlaceOfDeath(Enum):
    All = "*All*"
    MedicalFacilityInpatient = "1"
    MedicalFacilityOutpatient = "2"
    MedicalFacilityDeadOnArrival = "3"
    MedicalFacilityUnknownStatus = "10"
    DecedentHome = "4"
    HospiceFacility = "5"
    NursingHome = "6"
    Other = "7"
    Unknown = "9"

class Autopsy(Enum):
    All = "*All*"
    No = "N"
    Yes = "Y"
    Unknown = "U"
