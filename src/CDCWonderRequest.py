import typing
import requests

import CDCWonderResponse
from utils import dictToXML
from enums import XYZEnum

class CDCWonderRequest():
    """
    NOTE TO DEVS:
    + Always return self
    + Getters for each setting method
        ¿ Or a getter for entire internal state ?
    """

    def __init__(self, accept_datause_restrictions=False):
        """
        """

        if not accept_datause_restrictions:
            # TODO: Create custom exceptions for known errors like these.
            raise Exception("All access to data and statistics on CDC WONDER, "
                            "or subsequent re-use of that information, is subject to CDC's "
                            "data use restrictions policy. Please accept data use restrictions "
                            "to access the API.")

        # Initialize state with default parameter values.
        self.initDefaultParameters()



    def send(self) -> "CDCWonderResponse":
        """
        """

        # Build XML with parameter values from internal state.
        self.request_xml = "<request-parameters>\n"
        self.request_xml += dictToXML({"accept_datause_restrictions": "true"}) # Wouldn't be able to get here if they hadn't accepted
        self.request_xml += dictToXML(self.b_parameters)
        self.request_xml += dictToXML(self.m_parameters)
        self.request_xml += dictToXML(self.f_parameters)
        self.request_xml += dictToXML(self.i_parameters)
        self.request_xml += dictToXML(self.v_parameters)
        self.request_xml += dictToXML(self.o_parameters)
        self.request_xml += dictToXML(self.vm_parameters)
        self.request_xml += dictToXML(self.misc_parameters)
        self.request_xml += "</request-parameters>"

        url = "https://wonder.cdc.gov/controller/datarequest/D76"
        response = requests.post(url, data={"request_xml": self.request_xml})
        print(response.status_code) # TODO: Error handling
        print(response.text) # TODO: Response parsing


    def initDefaultParameters(self):
        """
        Initializes state to default parameter values.

        Best parameter reference: https://github.com/alipphardt/cdc-wonder-api/blob/master/README.md
        """

        # Group-by parameters.
        self.b_parameters = {
            "B_1": "D76.V1-level1",  # year
            "B_2": "*None*",
            "B_3": "*None*",
            "B_4": "*None*",
            "B_5": "*None*"
        }

        # Measures to return. Deaths, Population and Crude Rate are included by default (but must still be included).
        self.m_parameters = {
            "M_1": "D76.M1",  # Deaths, must be included
            "M_2": "D76.M2",  # Population, must be included
            "M_3": "D76.M3",  # Crude rate, must be included
            # Add any additional measures here.
        }

        # Values highlighted in a "Finder" control for hierarchical lists, such as the "Regions/Divisions/States/Counties hierarchical" list.
        # Format for F parameters: <year1> <year2> or <year1>/<month1> <year2>/<month2>
        self.f_parameters = {
            "F_D76.V1": ["*All*"],  # year/month # TODO: Why is this 1999 in the default example
            "F_D76.V10": ["*All*"],  # Census Regions - dont change
            "F_D76.V2": ["*All*"],  # ICD-10 Codes
            "F_D76.V27": ["*All*"],  # HHS Regions - dont change
            "F_D76.V9": ["*All*"]  # State County - dont change
        }

        # Contents of the "Currently selected" information areas next to "Finder" controls in the "Request Form."
        # Format for I parameters: <year> (<year>) or <year1>/<month1> (<month1 abbrev>., <year 1>) <year2>/<month2> (<month2 abbrev>., <year 2>)
        self.i_parameters = {
            "I_D76.V1": "*All* (All Dates)",  # year/month # TODO: Why is this 1999 in default example
            "I_D76.V10": "*All* (The United States)",  # Census Regions - dont change
            "I_D76.V2": "*All* (All Causes of Death)",  # Causes of Death
            "I_D76.V27": "*All* (The United States)",  # HHS Regions - dont change
            "I_D76.V9": "*All* (The United States)",  # State County - dont change
            "I_D76.V25": "All Causes of Death"  # TODO: This wasn't a parameter in jupyter notebook
        }

        # Variable values to limit in the "where" clause of the query, found in multiple select list boxes and advanced finder text boxes.
        # Format for V parameters: <year> (<year>) or <year1>/<month1> (<month1 abbrev>., <year 1>) <year2>/<month2> (<month2 abbrev>., <year 2>)
        self.v_parameters = {
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
            "V_D76.V25": "",  # Drug/Alcohol Induced Causes # TODO: Non-empty in jupyter notebook
            "V_D76.V27": "",  # HHS Regions
            "V_D76.V51": "*All*",  # Five-Year Age Groups
            "V_D76.V52": "*All*"  # Single-Year Ages
        }

        # Other parameters, such as radio buttons, checkboxes, and lists that are not data categories
        self.o_parameters = {
            # Fmode controls whether the parameters pull from regular (F) or advanced finder (V_) parameters.
            "O_V1_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_V2_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_V9_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_V10_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_V27_fmode": "freg",  # Use regular finder and ignore v parameter value
            "O_aar": "aar_none",  # age-adjusted rates
            "O_aar_pop": "0000",  # population selection for age-adjusted rates
            "O_age": "D76.V5",  # 10-year age groups (could be ten-year, five-year, single-year, infant groups)
            "O_javascript": "on",  # Set to on by default # TODO: off since not in browser?
            "O_location": "D76.V9",  # select location variable to use (states here, but could be census or hhs regions)
            "O_precision": "9",  # decimal places (max)
            "O_rate_per": "100000",  # rates calculated per X persons
            "O_show_totals": "true",  # Show totals
            "O_show_zeros": "true",  # Show zero values
            "O_timeout": "600",  # TODO: Do we care about data access timeout?
            "O_title": "",  # TODO: title for data run
            "O_ucd": "D76.V2",  # select underlying cause of death category (ICD-10 by default)
            "O_urban": "D76.V19"  # select urbanization category (2013 by default)
        }

        # Values for non-standard age adjusted rates (ignored if standard age adjusted rates are used)
        self.vm_parameters = {
            "VM_D76.M6_D76.V1_S": "*All*",  # Year
            "VM_D76.M6_D76.V7": "*All*",  # Gender
            "VM_D76.M6_D76.V8": "*All*",  # Race
            "VM_D76.M6_D76.V10": "",  # Location
            "VM_D76.M6_D76.V17": "*All*",  # Hispanic-Origin
        }

        # Miscellaneous hidden inputs/parameters usually passed by web form. These do not change.
        self.misc_parameters = {
            "action-Send": "Send",
            "finder-stage-D76.V1": "codeset",
            "finder-stage-D76.V2": "codeset",
            "finder-stage-D76.V27": "codeset",
            "finder-stage-D76.V9": "codeset",
            "stage": "request"
        }




    #########################################
    #### Organize Table Layout
    #########################################

    def set_grouping(self, *args):
        raise NotImplementedError


    #########################################
    #### Location
    #########################################

    def set_location(self, *args):
        """ Pass in some number of locations to union, method extracts the type from the arguments,
        raise an exception if one is mismatched (at time of location function call).

        e.g. location(HHSRegion.H1, HHSRegion.H2, States.NY) <-- not allowed
        """
        raise NotImplementedError

    def set_urbanization(self, *args):
        """
        """
        raise NotImplementedError


    #########################################
    #### Democraphic
    #########################################

    def set_age_groups(self, *args):
        """
        """
        raise NotImplementedError

    def set_gender(self, *args):
        """
        """
        raise NotImplementedError

    def set_race(self, *args):
        """
        """
        raise NotImplementedError

    def set_hispanic_origin(self, *args):
        """
        """
        raise NotImplementedError


    #########################################
    #### Chronology
    #########################################

    def set_dates(self, *args):
        """
        """
        raise NotImplementedError

    def set_weekday(self, *args):
        """
        """
        raise NotImplementedError


    #########################################
    #### Miscellaneous
    #########################################

    def set_place_of_death(self, *args):
        """
        """
        raise NotImplementedError

    def set_autopsy(self, *args):
        """
        """
        raise NotImplementedError

    def set_cause_of_death(self, *args):
        """
        """
        raise NotImplementedError





if __name__ == '__main__':
    # Sample Code
    req = CDCWonderRequest(accept_datause_restrictions=True)
    
    try:
        req.send()
    except Exception as e:
        print(e)
