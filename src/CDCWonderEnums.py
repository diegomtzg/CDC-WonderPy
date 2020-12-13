from enum import Enum

#Location enums

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
#Demographic data enums

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

#Chronology enums

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

#Miscellaneous data enums

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

