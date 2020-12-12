from enum import Enum

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

