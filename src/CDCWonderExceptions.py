class DataUseAgreementException(Exception):
    def __init__(self):
        super().__init__("All access to data and statistics on CDC WONDER, "
                         "or subsequent re-use of that information, is subject "
                         "to CDC's data use restrictions policy.\n"
                         "You can find the CDC's data use restrictions at: https://wonder.cdc.gov/datause.html\n"
                         "Please accept data use restrictions by calling the "
                         "CDCWonderRequest's accept_datause_restrictions() method.")