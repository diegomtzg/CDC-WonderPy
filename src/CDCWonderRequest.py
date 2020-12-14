import requests

from CDCWonderResponse import CDCWonderResponse
from utils import dictToXML
from CDCWonderEnums import *
from CDCWonderExceptions import *
from CDCWonderExceptionsPrivate import *


'''
#TODO - add documentation about Not Applicable/ Restricted limits
Refer to messenger chat
'''
class CDCWonderRequest():
    """
    NOTE TO DEVS:
    + Always return self
    + Getters for each setting method
        ¿ Or a getter for entire internal state ?
    """

    def __init__(self, debug_mode=False):
        """
        Initializes the internal state of this request builder with the
        default parameter values so that users can easily get the most general
        version of the data.

        Best parameter reference: https://github.com/alipphardt/cdc-wonder-api/blob/master/README.md
        """
        self._DEBUG = debug_mode

        # Group-by parameters.
        self._b_parameters = {
            "B_1": "D76.V1-level1",  # year
            "B_2": "*None*",
            "B_3": "*None*",
            "B_4": "*None*",
            "B_5": "*None*"
        }

        # Measures to return. Deaths, Population and Crude Rate are included by default (but must still be included).
        self._m_parameters = {
            "M_1": "D76.M1",  # Deaths, must be included
            "M_2": "D76.M2",  # Population, must be included
            "M_3": "D76.M3",  # Crude rate, must be included
            # Add any additional measures here.
        }

        # Values highlighted in a "Finder" control for hierarchical lists, such as the "Regions/Divisions/States/Counties hierarchical" list.
        # Format for F parameters: <year1> <year2> or <year1>/<month1> <year2>/<month2>
        self._f_parameters = {
            "F_D76.V1": ["*All*"],  # year/month
            "F_D76.V10": ["*All*"],  # Census Regions - dont change
            "F_D76.V2": ["*All*"],  # ICD-10 Codes
            "F_D76.V27": ["*All*"],  # HHS Regions - dont change
            "F_D76.V9": ["*All*"]  # State County - dont change
        }

        # Contents of the "Currently selected" information areas next to "Finder" controls in the "Request Form."
        # Format for I parameters: <year> (<year>) or <year1>/<month1> (<month1 abbrev>., <year 1>) <year2>/<month2> (<month2 abbrev>., <year 2>)
        self._i_parameters = {
            "I_D76.V1": "*All* (All Dates)",  # year/month
            "I_D76.V10": "*All* (The United States)",  # Census Regions - dont change
            "I_D76.V2": "*All* (All Causes of Death)",  # Causes of Death
            "I_D76.V27": "*All* (The United States)",  # HHS Regions - dont change
            "I_D76.V9": "*All* (The United States)",  # State County - dont change
            "I_D76.V25": "All Causes of Death"
        }

        # Variable values to limit in the "where" clause of the query, found in multiple select list boxes and advanced finder text boxes.
        # Format for V parameters: <year> (<year>) or <year1>/<month1> (<month1 abbrev>., <year 1>) <year2>/<month2> (<month2 abbrev>., <year 2>)
        self._v_parameters = {
            "V_D76.V1": "",  # Year/Month
            "V_D76.V2": "",  # ICD-10 Codes
            "V_D76.V4": "*All*",  # ICD-10 113 Cause List
            "V_D76.V5": "*All*",  # Ten-Year Age Groups
            "V_D76.V6": "00",  # Infant Age Groups
            "V_D76.V7": "*All*",  # Gender
            "V_D76.V8": "*All*",  # Race
            "V_D76.V9": "",  # State/County
            "V_D76.V10": "",  # Census Regions
            "V_D76.V11": "*All*",  # 2006 Urbanization
            "V_D76.V12": "*All*",  # ICD-10 130 Cause List (Infants)
            "V_D76.V17": "*All*",  # Hispanic Origin
            "V_D76.V19": "*All*",  # 2013 Urbanization
            "V_D76.V20": "*All*",  # Autopsy
            "V_D76.V21": "*All*",  # Place of Death
            "V_D76.V22": "*All*",  # Injury Intent
            "V_D76.V23": "*All*",  # Injury Mechanism and All Other Leading Causes
            "V_D76.V24": "*All*",  # Weekday
            "V_D76.V25": "",  # Drug/Alcohol Induced Causes
            "V_D76.V27": "",  # HHS Regions
            "V_D76.V51": "*All*",  # Five-Year Age Groups
            "V_D76.V52": "*All*"  # Single-Year Ages
        }

        # Other parameters, such as radio buttons, checkboxes, and lists that are not data categories
        self._o_parameters = {
            # Fmode controls whether the parameters pull from regular (F) or advanced finder (V_) parameters.
            "O_V1_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_V2_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_V9_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_V10_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_V27_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_aar": "aar_none",  # age-adjusted rates
            "O_aar_pop": "0000",  # population selection for age-adjusted rates
            "O_age": "D76.V5",  # 10-year age groups (could be ten-year, five-year, single-year, infant groups)
            "O_javascript": "on",  # Set to on by default # TODO: Off since not in browser?
            "O_location": "D76.V9",  # select location variable to use (states here, but could be census or hhs regions)
            "O_precision": "9",  # decimal places (max)
            "O_rate_per": "100000",  # rates calculated per X persons
            "O_show_totals": "true",  # Show totals
            "O_show_zeros": "true",  # Show zero values
            "O_timeout": "600",  # TODO: Do we care about data access timeout?
            "O_title": "",  # TODO: Do we want to set this title?
            "O_ucd": "D76.V2",  # select underlying cause of death category (ICD-10 by default)
            "O_urban": "D76.V19"  # select urbanization category (2013 by default)
        }

        # Values for non-standard age adjusted rates (ignored if standard age adjusted rates are used)
        self._vm_parameters = {
            "VM_D76.M6_D76.V1_S": "*All*",  # Year
            "VM_D76.M6_D76.V7": "*All*",  # Gender
            "VM_D76.M6_D76.V8": "*All*",  # Race
            "VM_D76.M6_D76.V10": "",  # Location
            "VM_D76.M6_D76.V17": "*All*",  # Hispanic-Origin
        }

        # Miscellaneous hidden inputs/parameters usually passed by web form. These do not change.
        self._misc_parameters = {
            "action-Send": "Send",
            "finder-stage-D76.V1": "codeset",
            "finder-stage-D76.V2": "codeset",
            "finder-stage-D76.V27": "codeset",
            "finder-stage-D76.V9": "codeset",
            "stage": "request"
        }


    def send(self) -> "CDCWonderResponse":
        """
        Builds an XML parameter document with the parameter values from the current internal state
        and sends a POST request to the CDC Wonder API.
        """

        request_xml = "<request-parameters>\n"
        request_xml += dictToXML({"accept_datause_restrictions": "true"})
        request_xml += dictToXML(self._b_parameters)
        request_xml += dictToXML(self._m_parameters)
        request_xml += dictToXML(self._f_parameters)
        request_xml += dictToXML(self._i_parameters)
        request_xml += dictToXML(self._v_parameters)
        request_xml += dictToXML(self._o_parameters)
        request_xml += dictToXML(self._vm_parameters)
        request_xml += dictToXML(self._misc_parameters)
        request_xml += "</request-parameters>"

        url = "https://wonder.cdc.gov/controller/datarequest/D76"
        response = requests.post(url, data={"request_xml": request_xml})
        print("This is the status code: " + str(response.status_code)) # TODO: Error handling    
        return CDCWonderResponse(response.text)


    #########################################
    #### Organize Table Layout
    #########################################

    def set_grouping(self, *args):
        raise NotImplementedError


    #########################################
    #### Location
    #########################################

    def set_location(self, *args):
        """ 
        Pass in a non-zero number of locations of the same location type
  
        @param self: is the instance this function is being called on.
        @param args: the location (States/CensusRegion/HHSRegion) options that the user wants to filter by
                    Note that all provided args must be of the same location type.
        returns: self

        Exceptions raised:
            ValueError if atleast one location isn't provided
            TypeError if arguments provided aren't of the same location type.
        """
        if (len(args) == 0):
            raise ValueError("Function expects atleast one argument")
        typeOfArgs = type(args[0])
        if (typeOfArgs not in [States, CensusRegion, HHSRegion]):
            raise TypeError("Provided arguments aren't any of type Stages, CensusRegion or HHSRegion")

        locations = set()
        for arg in args:
            if (type(arg) != typeOfArgs):
                raise TypeError("Mismatched location types provided. " + str(arg) + " doesn't match type of previous arguments. Please provide arguments of the same location type. For reference, check CDCWonderEnums.py")
            locations.add(arg.value) 
        self._f_parameters["F_D76.V9"] = list(locations)
        self._i_parameters["I_D76.V9"] = list(locations)
        return self

    def set_urbanization(self, *args):
        """
        """
        raise NotImplementedError


    #########################################
    #### Demographic
    #########################################

    def set_age_groups(self, *args):
        """
        """
        raise NotImplementedError

    def set_gender(self, gender):
        """
        Specify which Gender option to filter by. Default is *All*.

        @param self: is the instance this function is being called on.
        @param gender: the gender option that the user wants to filter by

        returns: self

        Exceptions raised:
            TypeError if argument "gender" provided isn't of type Gender
        """
        if (type(gender) != Gender):
            raise TypeError
        # TODO -> v or vm params?
        self._v_parameters["V_D76.V7"] = gender.value
        return self

    def set_race(self, *args):
        """
        Specify the Race options to filter by. Default is *All*.

        @param self: is the instance this function is being called on.
        @param args: the race options that the user wants to filter by

        returns: self

        Exceptions raised:
            ValueError if atleast one race isn't provided or if Race.All 
                        is provided with other Race options
            TypeError if arguments provided aren't of type Race
        """
        if (len(args) == 0):
            raise ValueError("Function expects atleast one Race")
        races = set()
        for arg in args:
            if (type(arg) != Race):
                raise TypeError("Provided arguments aren't of race enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            races.add(arg.value)
        if (len(races) > 1 and Race.All in races):
            raise ValueError(race_exception)
        self._v_parameters["V_D76.V8"] = list(races)
        return self

    def set_hispanic_origin(self, *args):
        """
        Specify the Hispanic origin options to filter by. Default is *All*.

        @param self: is the instance this function is being called on.
        @param args: the HispanicOrigin options that the user wants to filter by

        returns: self

        Exceptions raised:
            ValueError if atleast one HispanicOrigin isn't provided, or if HispanicOrigin.All 
                        is provided with other HispanicOrigin options
            TypeError if arguments provided aren't of type Race
        """
        if (len(args) == 0):
            raise ValueError("Function expects atleast one HispanicOrigin")
        hispanic_origins = set()
        for arg in args:
            if (type(arg) != HispanicOrigin):
                raise TypeError("Provided arguments aren't of Hispanic Origin enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            hispanic_origins.add(arg.value)
        if (len(hispanic_origins) > 1 and HispanicOrigin.All in hispanic_origins):
            raise ValueError(hispanic_origin_all_exception)
        if (len(hispanic_origins) > 1 and HispanicOrigin.NotStated in hispanic_origins):
            raise ValueError(hispanic_origin_ns_exception)        
        self._v_parameters["V_D76.V17"] = list(hispanic_origins)
        return self

    #########################################
    #### Chronology
    #########################################

    def set_dates(self, *args):
        """
        """
        raise NotImplementedError

    def set_weekday(self, *args):
        """
        Specify weekday options to filter by. Default is *All*.

        @param self: is the instance this function is being called on.
        @param args: the Weekday options that the user wants to filter by

        returns: self

        Exceptions raised:
            ValueError if atleast one Weekday option isn't provided, or if Weekday.All 
                        is provided with other Weekday options
            TypeError if arguments provided aren't of type Weekday
        """
        if (len(args) == 0):
            raise ValueError("Function expects atleast one Weekday")
        weekdays = set()
        for arg in args:
            if (type(arg) != Weekday):
                raise TypeError("Provided arguments aren't of Weekday enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            weekdays.add(arg.value)
        if (len(weekdays) > 1 and Weekday.All in weekdays):
            raise ValueError(weekday_exception)
        self._v_parameters["V_D76.V24"] = list(weekdays)
        return self

    #########################################
    #### Miscellaneous
    #########################################

    def set_place_of_death(self, *args):
        """
        Specify the Place of Death options to filter by. Default is *All*.

        @param self: is the instance this function is being called on.
        @param args: the PlaceOfDeath options that the user wants to filter by

        returns: self

        Exceptions raised:
            ValueError if atleast one PlaceOfDeath option isn't provided, or if PlaceOfDeath.All 
                        is provided with other PlaceOfDeath options
            TypeError if arguments provided aren't of type PlaceOfDeath
        """
        if (len(args) == 0):
            raise ValueError("Function expects atleast one Place Of Death")
        place_of_death_options = set()
        for arg in args:
            if (type(arg) != PlaceOfDeath):
                raise TypeError("Provided arguments aren't of PlaceOfDeath enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            place_of_death_options.add(arg.value)
        if (len(place_of_death_options) > 1 and PlaceOfDeath.All in place_of_death_options):
            raise ValueError(place_of_death_exception)
        self._v_parameters["V_D76.V21"] = list(place_of_death_options)
        return self


    def set_autopsy(self, *args):
        """
        Specify the Autopsy options to filter by. Default is *All*.

        @param self: is the instance this function is being called on.
        @param args: the Autopsy options that the user wants to filter by

        returns: self

        Exceptions raised:
            ValueError if atleast one Autopsy option isn't provided, or if Autopsy.All 
                        is provided with other Autopsy options
            TypeError if arguments provided aren't of type Autopsy
        """
        if (len(args) == 0):
            raise ValueError("Function expects atleast one Race")
        autopsy_options = set()
        for arg in args:
            if (type(arg) != Autopsy):
                raise TypeError("Provided arguments aren't of Autopsy enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            autopsy_options.add(arg.value)
        if (len(autopsy_options) > 1 and Autopsy.All in autopsy_options):
            raise ValueError(autopsy_exception)
        self._v_parameters["V_D76.V20"] = list(autopsy_options)
        return self

    def set_cause_of_death(self, *args):
        """
        """
        raise NotImplementedError


# Sample code
if __name__ == '__main__':
    req = CDCWonderRequest()
    # Example of setter
    req.set_hispanic_origin(HispanicOrigin.HispanicOrLatino, HispanicOrigin.NotHispanicOrLatino)
    # req.set_gender(Gender.Female).set_race(Race.Asian)
    # req.set_weekday(Weekday.Sun, Weekday.Mon, Weekday.Thu)
    # req.set_autopsy(Autopsy.Yes)
    # req.set_place_of_death(PlaceOfDeath.DecedentHome)
    req.set_location(States.Washington)
    response = req.send()
    #TODO-> status 500 is empty dataframe or error maybe?
    print(response.as_dataframe())
