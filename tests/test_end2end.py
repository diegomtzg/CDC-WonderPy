import cdcwonderpy as wonder
import unittest

# TODO -> add testing documentation
# End to end testing
class EndToEndTests(unittest.TestCase):
    def test1(self):
        req = wonder.Request()
        req.group_by(wonder.Grouping.GENDER)
        response = req.send()
        res2DList = response.as_2d_list()

        female_deaths_from_gui = 25324635
        male_deaths_from_gui = 25243139
        female_population = 3095193684
        male_population = 2993439317
        female_crude_rate = 818.2
        male_crude_rate = 843.3

        self.assertEqual(res2DList[0][0], "Female")
        self.assertEqual(res2DList[1][0], "Male")

        self.assertEqual(res2DList[0][1],female_deaths_from_gui)
        self.assertEqual(res2DList[1][1],male_deaths_from_gui)
        
        self.assertEqual(res2DList[0][2], female_population)
        self.assertEqual(res2DList[1][2], male_population)

        self.assertAlmostEqual(res2DList[0][3], female_crude_rate, places=1)
        self.assertAlmostEqual(res2DList[1][3], male_crude_rate, places=1)

    def test2(self):
        req = wonder.Request()
        req.group_by(wonder.Grouping.HISPANIC_ORIGIN)
        req.weekday(wonder.Weekday.SUN, wonder.Weekday.MON, wonder.Weekday.TUE)
        response = req.send()
        resDataFrame = response.as_dataframe()

        #Check that we get all desired column headings
        columnHeadings = list(resDataFrame.columns)
        self.assertEqual(columnHeadings[0], "HISPANIC_ORIGIN")
        self.assertEqual(columnHeadings[1], "Deaths")
        self.assertEqual(columnHeadings[2], "Population")
        self.assertEqual(columnHeadings[3], "Crude Rate Per 100,000")

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

        self.assertEqual(int(res2DList[0][1]), hispanic_or_latino_deaths_gui)
        self.assertEqual(int(res2DList[1][1]), not_hispanic_or_latino_deaths_gui)
        self.assertEqual(int(res2DList[2][1]), not_stated_deaths_gui)
        
        self.assertEqual(res2DList[0][2], hispanic_or_latino_population_gui)
        self.assertEqual(res2DList[1][2], not_hispanic_or_latino_population_gui)
        self.assertEqual(res2DList[2][2], not_stated_population_gui)

        self.assertEqual(res2DList[0][3], hispanic_or_latino_crude_rate_gui)
        self.assertEqual(res2DList[1][3], not_hispanic_or_latino_crude_rate_gui)
        self.assertEqual(res2DList[2][3], not_stated_crude_rate_gui)
