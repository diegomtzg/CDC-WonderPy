import WonderRequest
import WonderResponse
from WonderEnums import *
import bs4 as bs
import pandas as pd

#Testing parsing of response
class WonderResponseTest():
    
    @classmethod
    def test_as_2d_list(cls):
        pass
    
    @classmethod
    def test_as_dataframe(cls):
        pass

#End to end testing
class EndToEndTests():
    @classmethod
    def _float_is_almost_equal(cls, a, b, epsilon=0.1):
        return abs(a-b) <= epsilon

    @classmethod
    def test1(cls):
        req = WonderRequest.WonderRequest()
        req.group_by(Grouping.Gender)
        response = req.send()
        res2DList = response.as_2d_list()

        female_deaths_from_gui = 25324635
        male_deaths_from_gui = 25243139
        female_population = 3095193684
        male_population = 2993439317
        female_crude_rate = 818.2
        male_crude_rate = 843.3
        
        assert(res2DList[0][0] == "Female")
        assert(res2DList[1][0] == "Male")

        assert(int(res2DList[0][1] == female_deaths_from_gui))
        assert(int(res2DList[1][1] == male_deaths_from_gui))
        
        assert(int(res2DList[0][2] == female_population))
        assert(int(res2DList[1][2] == male_population))   

        assert(cls._float_is_almost_equal(res2DList[0][3],female_crude_rate))   
        assert(cls._float_is_almost_equal(res2DList[1][3],male_crude_rate))   

    @classmethod
    def test2(cls):
        req = WonderRequest.WonderRequest()
        req.group_by(Grouping.HispanicOrigin)
        req.weekday(Weekday.Sun, Weekday.Mon, Weekday.Tue)
        response = req.send()
        resDataFrame = response.as_dataframe()

        #Check that we get all desired column headings
        columnHeadings = list(resDataFrame.columns)
        assert(columnHeadings[0] == "HispanicOrigin")
        assert(columnHeadings[1] == "Deaths")
        assert(columnHeadings[2] == "Population")
        assert(columnHeadings[3] == "Crude Rate Per 100,000")

        res2DList = response.as_2d_list()

        hispanic_or_latino_deaths_gui = 1250489
        not_hispanic_or_latino_deaths_gui = 20268863	
        not_stated_deaths_gui = 59713
        hispanic_or_latino_population_gui = "Not Applicable"
        not_hispanic_or_latino_population_gui = "Not Applicable"
        not_stated_population_gui = "Not Applicable"
        hispanic_or_latino_crude_rate_gui = "Not Applicable"
        not_hispanic_or_latino_crude_rate_gui = "Not Applicable"
        not_stated_crude_rate_gui = "Not Applicable"

        assert(int(res2DList[0][1] == hispanic_or_latino_deaths_gui))
        assert(int(res2DList[1][1] == not_hispanic_or_latino_deaths_gui))
        assert(int(res2DList[2][1] == not_stated_deaths_gui))
        
        assert(int(res2DList[0][2] == hispanic_or_latino_population_gui))
        assert(int(res2DList[1][2] == not_hispanic_or_latino_population_gui))   
        assert(int(res2DList[2][2] == not_stated_population_gui))   

        assert(res2DList[0][3] == hispanic_or_latino_crude_rate_gui)   
        assert(res2DList[1][3] == not_hispanic_or_latino_crude_rate_gui)   
        assert(res2DList[2][3] == not_stated_crude_rate_gui)   

if __name__ == '__main__':
    EndToEndTests.test1()
    EndToEndTests.test2()