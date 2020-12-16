import cdcwonderpy as wonder
from cdcwonderpy.enums import *

if __name__ == '__main__':
    # response = cdcwonderpy.Request().place_of_death(PlaceOfDeath.DECEDENT_HOME).send()
    # print(response.as_dataframe())
    req = wonder.Request()
    req.group_by(Grouping.GENDER, Grouping.YEAR)
    req.weekday(wonder.Weekday.SUN, wonder.Weekday.MON, wonder.Weekday.TUE)
    response = req.send()
    print(response)

    # Let's say you now want to filter by Thursday instead, but still wanted to group by gender and year.
    # You could do this!

    req.weekday(Weekday.THU)
    response = req.send()
    # If you want to view your response as a 2dlist, here's what you can do!
    print(response.as_2d_list())