import requests
from requests import RequestException
import bs4 as bs

from WonderResponse import WonderResponse
from WonderEnums import *
from Dates import *


class WonderRequest():
    """
    * A wrapper around the CDC Wonder REST API, specific to the Underlying Cause of Death Dataset (D76).
    * This API provides similar access to the database, but removes the need to specify unnecessary
    * parameters, renames them so that they're easier to use and provides a utility class called
    * WonderResponse that contains useful data transformation methods to analyze the data in
    * different formats.
    *
    * NOTE: By using this API, users implicitly signify that they will abide by the terms of data
    * use stated here: https://wonder.cdc.gov/ucd-icd10.html
    *
    * All of the methods that modify the input parameters return self so they can be chained together.
    *
    * * Default modifiable parameters *
    * - Group by: Year
    * - Demographics: All ages, genders, races and hispanic origins.
    * - Years and Months: All (1999 through 2018)
    * - Weekdays: All
    * - Autopsy: All
    * - Place of Death: All
    * - Cause of Death: All ICD-10 Codes

    * * Default values that cannot be changed through this API *
    * - Measures: Deaths, Population, Crude Rate (changing this is out of scope for this project)
    * - Location/Urbanization: All (cannot be changed, see limitations above)
    *
    *******************************************************************************************
    * LIMITATION: ASSURANCE OF CONFIDENTIALITY
    *******************************************************************************************
    * |Suppressed|
    * Vital statistics data are suppressed due to confidentiality constraints, in order to
    * protect personal privacy. The term "Suppressed" replaces sub-national death counts,
    * births counts, death rates and associated confidence intervals and standard errors,
    * as well as corresponding population figures, when the figure represents zero to
    * nine (0-9) persons.
    *
    * |Unreliable|
    * Rates are marked as "unreliable" when the death count is less than 20.
    *
    * |Not Applicable|
    * Rates are marked as "not applicable" when the population denominator figure is
    * unavailable, such as persons of "not stated" or unknown age or Hispanic origin.
    *
    * For more information, see: https://wonder.cdc.gov/wonder/help/ucd.html
    *******************************************************************************************


    *******************************************************************************************
    * LIMITATION: VITAL STATISTICS POLICY FOR PUBLIC DATA SHARING
    *******************************************************************************************
    * Queries for mortality and births statistics cannot limit or group results by any
    * location field, such as Region, Division, State or County, or Urbanization.
    *
    * For example, in the D76 online database for Detailed Mortality 1999-2013, the location
    * fields are D76.V9, D76.V10 and D76.V27, and the urbanization fields are D76.V11 and
    * D76.V19. These 'sub-national" data fields cannot be grouped by or limited via the API,
    * although these fields are available in the web application.
    *
    * For more information, see: https://wonder.cdc.gov/wonder/help/WONDER-API.html
    *******************************************************************************************
    """

    def __init__(self):
        """
        Constructor method that initializes this request instance to the same default values as
        the API's web GUI on https://wonder.cdc.gov/ucd-icd10.html (see class documentation).
        """

        # Group-by parameters.
        self._b_parameters = {
            "B_1": "D76.V1-level1",  # year
            "B_2": "*None*",
            "B_3": "*None*",
            "B_4": "*None*",
            "B_5": "*None*"
        }

        # Group-by column names. For the purpose of formatting the API Response table.
        self._group_by_column_names = ["Year"]

        # Measures to return. Deaths, Population and Crude Rate are included by default (but must still be included).
        self._m_parameters = {
            "M_1": "D76.M1",   # Deaths, must be included
            "M_2": "D76.M2",   # Population, must be included
            "M_3": "D76.M3",   # Crude rate, must be included
        }

        # Values highlighted in a "Finder" control for hierarchical lists, such as the "Regions/Divisions/States/Counties hierarchical" list.
        # Format for F parameters: <year1> <year2> or <year1>/<month1> <year2>/<month2>
        self._f_parameters = {
            "F_D76.V1": ["*All*"],  # year/month
            "F_D76.V10": ["*All*"],  # Census Regions - dont change (see above for limitations)
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
            "O_show_totals": "false",  # Do now show totals
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


    def send(self) -> 'WonderResponse':
        """
        Sends this request to the CDC Wonder API endpoint and returns the response as a WonderResponse.
        :returns WonderResponse: represents the response of the server
        :raises RequestException: when the server responds with an error (see exception message for details).
        """
        request_xml = "<request-parameters>\n"
        request_xml += self._dictToXML({"accept_datause_restrictions": "true"})
        request_xml += self._dictToXML(self._b_parameters)
        request_xml += self._dictToXML(self._m_parameters)
        request_xml += self._dictToXML(self._f_parameters)
        request_xml += self._dictToXML(self._i_parameters)
        request_xml += self._dictToXML(self._v_parameters)
        request_xml += self._dictToXML(self._o_parameters)
        request_xml += self._dictToXML(self._vm_parameters)
        request_xml += self._dictToXML(self._misc_parameters)
        request_xml += "</request-parameters>"

        url = "https://wonder.cdc.gov/controller/datarequest/D76"
        response = requests.post(url, data={"request_xml": request_xml})

        # Raise exception based on response status code and server error messages.
        if response.status_code != 200:
            error_messages = bs.BeautifulSoup(response.text, "lxml").find_all("message")

            exception_message = ""
            for message in error_messages:
                exception_message = exception_message + message.contents[0] + "\n"

            raise RequestException("The server returned an error: " + exception_message)

        return WonderResponse(response.text, self._group_by_column_names)


    #########################################
    #### Organize Table Layout
    #########################################
    def group_by(self, *args) -> 'WonderRequest':
        """
        Groups API requested results by one to five filters ranging from demographics to
        dates to cause of death. Note that filtering by Months will cause Population and
        Crude Rate / 100k columns to be marked "Not Applicable".

        :param  args:       Table groupings by which the user can format the requested data.
        :returns:           self
        :raises ValueError: If user inputs less than one or greater than 5 arguments.
        :raises TypeError:  If inputted arguments are not all of type Grouping.
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one grouping argument.")
        elif (len(args) > 5):
            raise ValueError("Method expects at most 5 grouping arguments.")
        
        groupings = list()
        for arg in args:
            if (type(arg) != Grouping):
                raise TypeError("Provided argument is not of type Grouping.")
            elif arg.value not in groupings:
                groupings.append(arg)
        
        # Reset b_parameters and group_by_column_names
        self._group_by_column_names = []
        for b_param_key in self._b_parameters:
            self._b_parameters[b_param_key] = "*None*"

        for i, grouping in enumerate(groupings):
            b_param_key = "B_" + str(i+1)
            self._b_parameters[b_param_key] = grouping.value
            self._group_by_column_names.append(grouping.name)

        return self


    #########################################
    #### Demographic
    #########################################
    def age_groups(self, *args) -> 'WonderRequest':
        """
        """
        raise NotImplementedError


    def gender(self, *args) -> 'WonderRequest':
        """
        Specify which Gender option to filter by.
        :param gender:      the gender option that the user wants to filter by
        :returns:           self
        :raises ValueError: if at least one race isn't provided or if Gender.All
        is provided with other Gender options.
        :raises TypeError:  if arguments provided aren't of type Gender
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Gender value.")
        gender_options = set()
        for arg in args:
            if (type(arg) != Gender):
                raise TypeError("Provided arguments aren't of Gender enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            gender_options.add(arg.value)
        if (len(gender_options) > 1 and Gender.All in gender_options):
            raise ValueError("Gender has both 'All Genders' and other options selected. Please select either 'All' or specific options.")
        self._v_parameters["V_D76.V7"] = list(gender_options)
        return self


    def race(self, *args) -> 'WonderRequest':
        """
        Specify the Race options to filter by.
        :param args:         the race options that the user wants to filter by
        :returns:            self
        :raises: ValueError: if at least one race isn't provided or if Race.All is provided with other Race options
        :raises TypeError:   if arguments provided aren't of type Race
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Race value.")
        races = set()
        for arg in args:
            if (type(arg) != Race):
                raise TypeError("Provided arguments aren't of race enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            races.add(arg.value)
        if (len(races) > 1 and Race.All in races):
            raise ValueError("Race has both 'All' and other options selected. Please select either 'All' or specific options.")
        self._v_parameters["V_D76.V8"] = list(races)
        return self


    def hispanic_origin(self, *args) -> 'WonderRequest':
        """
        Specify the Hispanic origin options to filter by.
        :param args:        the HispanicOrigin options that the user wants to filter by
        :returns:           self
        :raises ValueError: if at least one HispanicOrigin isn't provided, or if HispanicOrigin.All
                            is provided with other HispanicOrigin options
        :raises TypeError:  if arguments provided aren't of type Race
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one HispanicOrigin value.")
        hispanic_origins = set()
        for arg in args:
            if (type(arg) != HispanicOrigin):
                raise TypeError("Provided arguments aren't of Hispanic Origin enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            hispanic_origins.add(arg.value)
        if (len(hispanic_origins) > 1 and HispanicOrigin.All in hispanic_origins):
            raise ValueError("Hispanic Origin has both 'All' and other options selected. Please select either 'All' or specific options.")
        if (len(hispanic_origins) > 1 and HispanicOrigin.NotStated in hispanic_origins):
            raise ValueError("Hispanic Origin has both 'All' and other options selected. Please select either 'All' or specific options.")
        self._v_parameters["V_D76.V17"] = list(hispanic_origins)
        return self


    #########################################
    #### Chronology
    #########################################
    def dates(self, *args) -> 'WonderRequest':
        """
        Specify the dates to filter by. See the Dates class for more information on
        how dates can be specified as either single Year/Month or a range.
        :param args:        a list of either of dates of ranges of dates to filter by
        :returns:           self
        :raises ValueError: if at least one Date isn't provided, or if the specified date is
                            outside of 1999 - 2018 (range of the data).
        :raises TypeError:  if arguments provided aren't of type Dates
        """
        if len(args) == 0:
            raise ValueError("Method expects at least one value specifying the desired dates")

        total = Dates()
        for arg in args:
            if not isinstance(arg, Dates):
                raise TypeError("Provided arguments are not Dates objects. Please create Dates objects to set the year(s) and month(s) you would like to retrieve data from.")
            if any(e.is_before(Year(1999)) or e.is_after(Year(2018)) for e in arg.get_months()):
                raise ValueError("All dates must be between 1999 and 2018")
            total = Dates.union(total, arg)

        all_months = sorted(total.get_months())
        curr_year = None
        curr_year_set = set()
        date_params = set()
        for month in all_months:
            if curr_year != month.get_year():
                date_params.update(curr_year_set)
                curr_year_set = set()
                curr_year = month.get_year()
            
            curr_year_set.add(month)
            
            if len(curr_year_set) == YearAndMonth.NUM_MONTHS:
                date_params.add(Year(curr_year))
                curr_year_set = set()

        date_params.update(curr_year_set)
        date_params_list = [str(e) for e in date_params]
        self._f_parameters["F_D76.V1"] = sorted(date_params_list)
        return self


    def weekday(self, *args) -> 'WonderRequest':
        """
        Specify weekday options to filter by. Default is *All*.
        :param args:        the Weekday options that the user wants to filter by
        :returns:           self
        :raises ValueError: if at least one Weekday option isn't provided, or if
                            Weekday.All is provided with other Weekday options
        :raises TypeError:  if arguments provided aren't of type Weekday
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Weekday value.")
        weekdays = set()
        for arg in args:
            if (type(arg) != Weekday):
                raise TypeError("Provided arguments aren't of Weekday enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            weekdays.add(arg.value)
        if (len(weekdays) > 1 and Weekday.All in weekdays):
            raise ValueError("PlaceOfDeath has both 'All' and other options selected. Please select either 'All' or specific options.")
        self._v_parameters["V_D76.V24"] = list(weekdays)
        return self


    #########################################
    #### Miscellaneous
    #########################################
    def place_of_death(self, *args) -> 'WonderRequest':
        """
        Specify the Place of Death options to filter by. Default is *All*.
        :param args:        the PlaceOfDeath options that the user wants to filter by
        :returns:           self
        :raises ValueError: if at least one PlaceOfDeath option isn't provided, or if PlaceOfDeath.All
                            is provided with other PlaceOfDeath options
        :raises TypeError:  if arguments provided aren't of type PlaceOfDeath
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Place of Death value.")
        place_of_death_options = set()
        for arg in args:
            if (type(arg) != PlaceOfDeath):
                raise TypeError("Provided arguments aren't of PlaceOfDeath enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            place_of_death_options.add(arg.value)
        if (len(place_of_death_options) > 1 and PlaceOfDeath.All in place_of_death_options):
            raise ValueError("PlaceOfDeath has both 'All' and other options selected. Please select either 'All' or specific options.")
        self._v_parameters["V_D76.V21"] = list(place_of_death_options)
        return self


    def autopsy(self, *args) -> 'WonderRequest':
        """
        Specify the Autopsy options to filter by. Default is *All*.
        :param args: the Autopsy options that the user wants to filter by
        :returns: self
        :raises ValueError: if at least one Autopsy option isn't provided, or if Autopsy.All is provided with other Autopsy options
        :raises TypeError: if arguments provided aren't of type Autopsy
        """
        if (len(args) == 0):
            raise ValueError("Method expects at least one Autopsy value.")
        autopsy_options = set()
        for arg in args:
            if (type(arg) != Autopsy):
                raise TypeError("Provided arguments aren't of Autopsy enum type. Please provide arguments of the right type. For reference, check CDCWonderEnums.py")
            autopsy_options.add(arg.value)
        if (len(autopsy_options) > 1 and Autopsy.All in autopsy_options):
            raise ValueError("Autopsy has both 'All' and other options selected. Please select either 'All' or specific options.")
        self._v_parameters["V_D76.V20"] = list(autopsy_options)
        return self


    def cause_of_death(self, *args) -> 'WonderRequest':
        """
        """
        # TODO(@joel)
        raise NotImplementedError

    ##################################
    # Private internal helper methods
    ##################################
    @staticmethod
    def _dictToXML(parameterDict):
        """
        Private helper function that transforms a dictionary single parameter -> value
        mappings to an equivalent XML string representation.
        """
        parameterString = ""
        for key in parameterDict:
            parameterString += "<parameter>\n"
            parameterString += "<name>" + key + "</name>\n"

            # If value is a list, concatenate all values
            if isinstance(parameterDict[key], list) or isinstance(parameterDict[key], tuple):
                for value in parameterDict[key]:
                    parameterString += "<value>" + value + "</value>\n"
            else:
                parameterString += "<value>" + parameterDict[key] + "</value>\n"

            parameterString += "</parameter>\n"

        return parameterString


# Sample code
if __name__ == '__main__':
    req = WonderRequest()
    # req.dates(Dates.range(Year(2001), Year(2003)), Dates.single(YearAndMonth(2005, 4)), Dates.range(YearAndMonth(2003, 6), YearAndMonth(2004, 9)))
    # req.hispanic_origin(HispanicOrigin.HispanicOrLatino, HispanicOrigin.NotHispanicOrLatino)
    # req.gender(Gender.Female).race(Race.Asian)
    # req.weekday(Weekday.Sun, Weekday.Mon, Weekday.Thu)
    # req.autopsy(Autopsy.Yes)
    # req.place_of_death(PlaceOfDeath.DecedentHome)
    req.group_by(Grouping.Gender, Grouping.Month)

    response = req.send()
    print(response.as_dataframe())
