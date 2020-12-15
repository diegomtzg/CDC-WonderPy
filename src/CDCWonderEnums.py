from enum import Enum

#########################################
#### Grouping Enums
#########################################

class Grouping(Enum):
    # Location
    CensusRegion = "D76.V10-level1"
    CensusDivision = "D76.V10-level2"
    HHSRegion = "D76.V27-level1"
    State = "D76.V9-level1"
    County = "D76.V9-level2"
    Urbanization2013 = "D76.V19"
    Urbanization2006 = "D76.V11"

    # Demographics
    AgeGroups = "D76.V5"
    Gender = "D76.V7"
    HispanicOrigin = "D76.V17"
    Race = "D76.V8"

    # Year and Month
    Year = "D76.V1-level1"
    Month = "D76.V1-level2"

    # Weekday, Autopsy, Place of Death
    Weekday = "D76.V24"
    Autopsy = "D76.V20"
    PlaceOfDeath = "D76.V21"

    # Cause of Death
    LeadingCausesOfDeath = "D76.V28"
    LeadingCausesOfInfantDeath = "D76.V29"
    ICDChapter = "D76.V2-level1"
    ICDSubChapter = "D76.V2-level2"
    CauseOfDeath = "D76.V2-level3"
    ICD10CauseList113 = "D76.V4"
    # ICD10InfantCauseList130 = "D76.V12"
    InjuryIntent = "D76.V22"
    InjuryMechanismAndAllOtherLeadingCauses = "D76.V23"
    DrugOrAlcoholInducedCauses = "D76.V25"

#########################################
#### Region Enums
#########################################
class States(Enum):
    All = "*All*"
    Alabama = "1" 
    Alaska = "2" 
    Arizona = "4"
    Arkansas = "5" 
    California = "6" 
    Colorado = "8"
    Connecticut = "9" 
    Delaware = "10"
    District_of_Columbia = "11"
    Florida = "12"
    Georgia = "13"
    Hawaii = "15"
    Idaho = "16"
    Illinois = "17"
    Indiana = "18"
    Iowa = "19"
    Kansas = "20"
    Kentucky = "21"
    Louisiana = "22"
    Maine = "23"
    Maryland = "24"
    Massachusetts = "25"
    Michigan = "26"
    Minnesota = "27"
    Mississippi = "28"
    Missouri = "29"
    Montana = "30"
    Nebraska = "31"
    Nevada = "32"
    New_Hampshire = "33"
    New_Jersey = "34"
    New_Mexico = "35"
    New_York = "36"
    North_Carolina = "37"
    North_Dakota = "38"
    Ohio = "39"
    Oklahoma = "40"
    Oregon = "41"
    Pennsylvania = "42"
    Rhode_Island = "44"
    South_Carolina = "45"
    South_Dakota = "46"
    Tennessee = "47"
    Texas = "48"
    Utah = "49"
    Vermont = "50"
    Virginia = "51"
    Washington = "53"
    West_Virginia = "54"
    Wisconsin = "55"
    Wyoming = "56"

class CensusRegion(Enum):
    All = "*All*"
    NorthEast = "CENS-R1"
    MidWest = "CENS-R2"
    South = "CENS-R3"
    West = "CENS-R4"

class HHSRegion(Enum):
    All = "*All*"
    HHSRegion1 = "HHS1"
    HHSRegion2 = "HHS2"
    HHSRegion3 = "HHS3"
    HHSRegion4 = "HHS4"
    HHSRegion5 = "HHS5"
    HHSRegion6 = "HHS6"
    HHSRegion7 = "HHS7"
    HHSRegion8 = "HHS8"
    HHSRegion9 = "HHS9"
    HHSRegion10 = "HHS10"

class UrbanizationYear(Enum):
    Year2013 = "D76.V19"
    Year2006 = "D76.V11"

class UrbanizationCategory(Enum):
    All = "*All*"
    LargeCentralMetro = "1"
    LargeFringeMetro = "2"
    MediumMetro = "3"
    SmallMetro = "4"
    Micropolitan = "5"
    NonCore = "6"

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
    AmericanIndian = "1002-5"
    Asian = "A-PI"
    AfricanAmerican = "2054-5"
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

