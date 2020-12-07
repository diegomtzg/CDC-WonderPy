import typing
from src.enums.XYZEnum import XYZ

class CDCWonderRequest(Object):
    """

    NOTE TO DEVS:
    + Always return self
    + Getters for each setting method
        ¿ Or a getter for entire internal state ?
    """

    def __init__(self, accept_datause_restrictions):
        """
        Default grouping: 'Census Region'
        Precision: 9 decimal points
        Show totals: True
        """
        self.accept_datause_restrictions = accept_datause_restrictions

        self.grouping_args = set([]) # Default `Census Region`
        self.location_args = set([])
        self.BLANK1_args = set([])
        self.BLANK2_args = set([])
        self.BLANK3_args = set([])
        self.BLANK4_args = set([])
        self.BLANK5_args = set([])

    def __str__(self):
        return ''

    def send(self) -> "CDCWonderResponse":
        """
        """
        raise NotImplementedError


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
        print(XYZ.X)
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
    
    req.group_by().location(XYZ.X)


    try:
        req.send()
    except:
        # We should hopefully not require users to write this except here
        pass
