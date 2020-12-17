import setup
import cdcwonderpy as wonder
from cdcwonderpy.dates import *
from cdcwonderpy.ages import *
from cdcwonderpy.icd10code import *
from cdcwonderpy.enums import *

"""
    Example of a query with multiple levels of complexity. It includes formatting
    parameters, multiple group-by specifications and multiple filters. The
    intention of this example is to show the flexibility of the API -- allowing
    users to both get simple data from it with ease but also specify complex
    parameters without a lot of boilerplate code and cryptic parameter names.
    
    Here, we want to group the results by month and ten-year age groups, and we want to filter results to only include
    the deaths caused by either ear or throat disease among people aged 15 to 74 every six months from January 2001 to
    July 2003. We then want to see the results as a dataframe.
    """
req = wonder.Request()
req.dates(Dates.single(YearAndMonth(2001, 1)), Dates.single(YearAndMonth(2001, 7)), Dates.single(YearAndMonth(2002, 1)), \
						Dates.single(YearAndMonth(2002, 7)), Dates.single(YearAndMonth(2003, 1)), Dates.single(YearAndMonth(2003, 7)))
req.cause_of_death(ICD10Code.description_matches_regex("disease.*( ear(\W+|$)| throat(\W+|$))", re.I))
req.age_groups(Ages.range(15, 74))
req.group_by(Grouping.MONTH, Grouping.TEN_YEAR_AGE_GROUPS)
response = req.send()
print(response.as_dataframe())
