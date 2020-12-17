import cdcwonderpy as wonder
from cdcwonderpy.enums import *

"""
Example of a query with multiple levels of complexity. It includes formatting
parameters, multiple group-by specifications and multiple filters. The
intention of this example is to show the flexibility of the API -- allowing
users to both get simple data from it with ease but also specify complex
parameters without a lot of boilerplate code and cryptic parameter names.

Here, we want to group by gender and year, and want to filter results to only
the deaths that happened on a weekend. We then want to see the results as a
2D list.
"""
req = wonder.Request()
req.group_by(Grouping.GENDER, Grouping.YEAR)
req.weekday(Weekday.SAT, Weekday.SUN)
response = req.send()
print(response.as_2d_list())