import cdcwonderpy as wonder
import bs4 as bs
import pandas as pd
import cdcwonderpy as wonder

req = wonder.Request()
req.group_by(wonder.Grouping.Gender)
req.weekday(wonder.Weekday.Sun, wonder.Weekday.Mon, wonder.Weekday.Tue)
response = req.send()
res2DList = response.as_2d_list()
print(res2DList)
