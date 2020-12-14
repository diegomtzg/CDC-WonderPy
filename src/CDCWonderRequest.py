import requests
from CDCWonderResponse import CDCWonderResponse
from utils import dictToXML
from CDCWonderEnums import *
from ExceptionMessages import *


class CDCWonderRequest():
    """

    TODO: Add documentation about Not Applicable/Restricted limits
    TODO: Add documentation about not being able to group by location and urbanization
    Population and rates are labeled 'Not Applicable' when Autopsy, Place of Death, Weekday or
    Month are grouped by or limited, due to lack of a valid population.
    """

    def __init__(self, debug_mode=False):
        """
        Initializes the internal state of this request builder with the
        default parameter values so that users can easily get the most general
        version of the data.
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
            "O_javascript": "on",  # Set to on by default
            "O_location": "D76.V9",  # select location variable to use (states here, but could be census or hhs regions)
            "O_precision": "9",  # decimal places (max)
            "O_rate_per": "100000",  # rates calculated per X persons
            "O_show_totals": "true",  # Show totals
            "O_show_zeros": "true",  # Show zero values
            "O_timeout": "600",
            "O_title": "CDCWonderAPI Request",
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
        TODO: I don't think we should mention that this builds an xml parameter document, that's an implementation detail
        Previously ->Builds an XML parameter document with the parameter values from the current internal state
        and sends a POST request to the CDC Wonder API.
        I propose -> Sends a request to the CDCWonder API and returns ??? (or something of this sort)
        :returns: a CDCWonderResponse object representing the request for the response
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

        # TODO: Error handling based on response.status_code
        print(request_xml)
        print("This is the status code: " + str(response.status_code))
        print(response.text)

        return CDCWonderResponse(response.text)


    #########################################
    #### Organize Table Layout
    #########################################
    def grouping(self, *args):
        raise NotImplementedError

    #########################################
    #### Location
    #########################################
    def region(self, *args):
        """ 
        Pass in a non-zero number of locations of the same location type
        :param args: the location (States/CensusRegion/HHSRegion) options that the user wants to filter by
                    Note that all provided args must be of the same location type.
        :returns: self
        :raises: ValueError if at least one location isn't provided
                 TypeError if arguments provided aren't of the same location type.
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one location argument.")
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

    def urbanization(self, urbanization_year, *args):
        """
        Pass in a non-zero number of locations of the same location type
        :param urbanization_year: the urbanization year to filter by
        :param args: the urbanization categories that the user wants to filter by
        :returns: self
        :raises: ValueError if at least one urbanization category isn't provided
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one urbanization argument.")

        # TODO: Only national data are available for this dataset when using the WONDER web service. Please check that your query does not group results by region, division, state, county or urbanization, (B_1 through B_5), nor limit these location variables to any specific values.

        categories = set()
        for arg in args:
           categories.add(arg.value)
        self._o_parameters["O_urban"] = urbanization_year.value
        if urbanization_year == urbanization_year.Year2013:
            self._v_parameters["V_D76.V19"] = list(categories)
        else:
            self._v_parameters["V_D76.V11"] = list(categories)
        return self


    #########################################
    #### Demographic
    #########################################

    def age_groups(self, *args):
        """
        """
        raise NotImplementedError

    def gender(self, *args):
        """
        Specify which Gender option to filter by. Default is *All*.
        :param gender: the gender option that the user wants to filter by
        :returns: self
        :raises: ValueError if at least one race isn't provided or if Gender.All
                        is provided with other Gender options
                 TypeError if arguments provided aren't of type Gender
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Gender value.")
        gender_options = set()
        for arg in args:
            if (type(arg) != Gender):
                raise TypeError("Provided arguments aren't of Gender enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            gender_options.add(arg.value)
        if (len(gender_options) > 1 and Gender.All in gender_options):
            raise ValueError(gender_exception)
        # TODO -> v or vm params?
        self._v_parameters["V_D76.V7"] = list(gender_options)
        return self

    def race(self, *args):
        """
        Specify the Race options to filter by. Default is *All*.
        :param args: the race options that the user wants to filter by
        :returns: self
        :raises: ValueError if at least one race isn't provided or if Race.All
                        is provided with other Race options
                 TypeError if arguments provided aren't of type Race
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Race value.")
        races = set()
        for arg in args:
            if (type(arg) != Race):
                raise TypeError("Provided arguments aren't of race enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            races.add(arg.value)
        if (len(races) > 1 and Race.All in races):
            raise ValueError(race_exception)
        self._v_parameters["V_D76.V8"] = list(races)
        return self

    def hispanic_origin(self, *args):
        """
        Specify the Hispanic origin options to filter by. Default is *All*.
        :param args: the HispanicOrigin options that the user wants to filter by
        :returns: self
        :raises: ValueError if at least one HispanicOrigin isn't provided, or if HispanicOrigin.All
                        is provided with other HispanicOrigin options
                 TypeError if arguments provided aren't of type Race
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one HispanicOrigin value.")
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
    def dates(self, *args):
        """
        """
        raise NotImplementedError

    def weekday(self, *args):
        """
        Specify weekday options to filter by. Default is *All*.
        :param args: the Weekday options that the user wants to filter by
        :returns: self
        :raises: ValueError if at least one Weekday option isn't provided, or if Weekday.All
                        is provided with other Weekday options
                 TypeError if arguments provided aren't of type Weekday
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Weekday value.")
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

    def place_of_death(self, *args):
        """
        Specify the Place of Death options to filter by. Default is *All*.
        :param args: the PlaceOfDeath options that the user wants to filter by
        :returns: self
        :raises: ValueError if at least one PlaceOfDeath option isn't provided, or if PlaceOfDeath.All
                        is provided with other PlaceOfDeath options
                 TypeError if arguments provided aren't of type PlaceOfDeath
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Place of Death value.")
        place_of_death_options = set()
        for arg in args:
            if (type(arg) != PlaceOfDeath):
                raise TypeError("Provided arguments aren't of PlaceOfDeath enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            place_of_death_options.add(arg.value)
        if (len(place_of_death_options) > 1 and PlaceOfDeath.All in place_of_death_options):
            raise ValueError(place_of_death_exception)
        self._v_parameters["V_D76.V21"] = list(place_of_death_options)
        return self


    def autopsy(self, *args):
        """
        Specify the Autopsy options to filter by. Default is *All*.
        :param args: the Autopsy options that the user wants to filter by
        :returns: self
        :raises: ValueError if at least one Autopsy option isn't provided, or if Autopsy.All
                        is provided with other Autopsy options
                 TypeError if arguments provided aren't of type Autopsy
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Autopsy value.")
        autopsy_options = set()
        for arg in args:
            if (type(arg) != Autopsy):
                raise TypeError("Provided arguments aren't of Autopsy enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            autopsy_options.add(arg.value)
        if (len(autopsy_options) > 1 and Autopsy.All in autopsy_options):
            raise ValueError(autopsy_exception)
        self._v_parameters["V_D76.V20"] = list(autopsy_options)
        return self

    def cause_of_death(self, *args):
        """
        """
        raise NotImplementedError


# Sample code
if __name__ == '__main__':
    req = CDCWonderRequest()
    # req.hispanic_origin(HispanicOrigin.HispanicOrLatino, HispanicOrigin.NotHispanicOrLatino)
    # req.gender(Gender.Female).race(Race.Asian)
    # req.weekday(Weekday.Sun, Weekday.Mon, Weekday.Thu)
    #req.autopsy(Autopsy.Yes)
    # req.place_of_death(PlaceOfDeath.DecedentHome)
    # req.region(States.Washington) # TODO: Doesn't work?

    # TODO: Passing year here looks confusing (how to tell it apart from other two args? maybe set urbanization year with separate method?)
    # req.urbanization(urbanization_year.Year2013, UrbanizationCategory.LargeCentralMetro, UrbanizationCategory.LargeFringeMetro)

    response = req.send()
    print(response.as_dataframe())
