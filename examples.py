import cdcwonderpy as wonder
from cdcwonderpy.enums import *
import bs4 as bs
import pandas as pd

req = wonder.Request()
req.group_by(Grouping.Gender, Grouping.Year)
# req.weekday(wonder.Weekday.Sun, wonder.Weekday.Mon, wonder.Weekday.Tue)
response = req.send()
res2DList = response.as_2d_list()
print(res2DList)
