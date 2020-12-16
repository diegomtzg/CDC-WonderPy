import cdcwonderpy as wonder
from cdcwonderpy.enums import *
import bs4 as bs

# The following code queries information about deaths on Sunday, Monday and Tuesday.
# It also groups results by gender and year
req = wonder.Request()
req.group_by(Grouping.Gender, Grouping.Year)
req.weekday(wonder.Weekday.Sun, wonder.Weekday.Mon, wonder.Weekday.Tue)
response = req.send()
print(response)

# Let's say you now want to filter by Thursday instead, but still wanted to group by gender and year. 
# You could do this!

req.weekday(Weekday.Thu)
response = req.send()
# If you want to view your response as a 2dlist, here's what you can do!
print(response.as_2d_list())


# Date examples

# ICD10 codes example
