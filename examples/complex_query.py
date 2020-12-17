import cdcwonderpy as wonder
from cdcwonderpy.enums import *
from cdcwonderpy.icd10code import ICD10Code

"""
    Example of a query with multiple levels of complexity. It includes formatting
    parameters, multiple group-by specifications and multiple filters. The
    intention of this example is to show the flexibility of the API -- allowing
    users to both get simple data from it with ease but also specify complex
    parameters without a lot of boilerplate code and cryptic parameter names.
    
    Here, we want to group the results by gender and year, and want to filter results to only include
    the deaths caused by nervous system diseases that occurred on a weekend. We then want to see the results as a
    2D list.
    """
req = wonder.Request()
req.group_by(Grouping.GENDER, Grouping.YEAR)
req.weekday(Weekday.SAT, Weekday.SUN)
req.cause_of_death(ICD10Code.description_best_match("Diseases of the nervous system"))
response = req.send()
print(response.as_2d_list())
