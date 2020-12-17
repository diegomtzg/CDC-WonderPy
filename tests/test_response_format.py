import cdcwonderpy as wonder
import unittest
import bs4 as bs
import pandas as pd

# Testing parsing of response
class ResponseFormattingTests(unittest.TestCase):
    sample_xml = open("tests/sample_response.xml").read()

    def test_as_2d_list(self):
        response = wonder.Response(ResponseFormattingTests.sample_xml, ["Year", "Race"])
        expected_result = [['1999', 'American Indian or Alaska Native', 210.0, 1375207.0, 15.270428379],
        ['1999', 'Asian or Pacific Islander', 73.0, 5813970.0, 1.255596434],
        ['1999', 'Black or African American', 1176.0, 17026405.0, 6.906918989],
        ['1999', 'White', 5067.0, 99715532.0, 5.081455114],
        ['2000', 'American Indian or Alaska Native', 213.0, 1438695.0, 14.805083774],
        ['2000', 'Asian or Pacific Islander', 87.0, 6003531.0, 1.449147177],
        ['2000', 'Black or African American', 1191.0, 17113752.0, 6.959315526],
        ['2000', 'White', 5098.0, 99668164.0, 5.114973323],
        ['2001', 'American Indian or Alaska Native', 222.0, 1495710.0, 14.842449405],
        ['2001', 'Asian or Pacific Islander', 88.0, 6307711.0, 1.395117817],
        ['2001', 'Black or African American', 1122.0, 17301249.0, 6.485080933],
        ['2001', 'White', 5002.0, 99632174.0, 5.020466581],
        ['2002', 'American Indian or Alaska Native', 241.0, 1545161.0, 15.597080175],
        ['2002', 'Asian or Pacific Islander', 94.0, 6538009.0, 1.437746568],
        ['2002', 'Black or African American', 993.0, 17420137.0, 5.700299602],
        ['2002', 'White', 5138.0, 99341123.0, 5.17207763],
        ['2003', 'American Indian or Alaska Native', 232.0, 1595470.0, 14.541169687],
        ['2003', 'Asian or Pacific Islander', 75.0, 6746797.0, 1.111638604],
        ['2003', 'Black or African American', 1012.0, 17521869.0, 5.775639574],
        ['2003', 'White', 4986.0, 98922719.0, 5.040298175],
        ['2004', 'American Indian or Alaska Native', 219.0, 1650247.0, 13.270740683],
        ['2004', 'Asian or Pacific Islander', 106.0, 6958064.0, 1.523412259],
        ['2004', 'Black or African American', 960.0, 17696877.0, 5.424685949],
        ['2004', 'White', 4639.0, 98709755.0, 4.699636829],
        ['2005', 'American Indian or Alaska Native', 219.0, 1705523.0, 12.840635981],
        ['2005', 'Asian or Pacific Islander', 100.0, 7166644.0, 1.39535325],
        ['2005', 'Black or African American', 801.0, 17868165.0, 4.482833016],
        ['2005', 'White', 4468.0, 98470022.0, 4.537421551],
        ['2006', 'American Indian or Alaska Native', 217.0, 1764276.0, 12.299662865],
        ['2006', 'Asian or Pacific Islander', 106.0, 7388679.0, 1.434627218],
        ['2006', 'Black or African American', 783.0, 18066694.0, 4.333941783],
        ['2006', 'White', 4462.0, 98263175.0, 4.540866912],
        ['2007', 'American Indian or Alaska Native', 257.0, 1822336.0, 14.102777973],
        ['2007', 'Asian or Pacific Islander', 86.0, 7595385.0, 1.132266501],
        ['2007', 'Black or African American', 770.0, 18244021.0, 4.220560807],
        ['2007', 'White', 4396.0, 97993766.0, 4.48599965],
        ['2008', 'American Indian or Alaska Native', 283.0, 1881082.0, 15.044532881],
        ['2008', 'Asian or Pacific Islander', 115.0, 7783988.0, 1.477391794],
        ['2008', 'Black or African American', 760.0, 18412297.0, 4.127676194],
        ['2008', 'White', 4460.0, 97714084.0, 4.564336908],
        ['2009', 'American Indian or Alaska Native', 259.0, 1937705.0, 13.366327692],
        ['2009', 'Asian or Pacific Islander', 118.0, 7960516.0, 1.48231597],
        ['2009', 'Black or African American', 711.0, 18548182.0, 3.833259777],
        ['2009', 'White', 4454.0, 97341682.0, 4.575634927],
        ['2010', 'American Indian or Alaska Native', 287.0, 1980311.0, 14.49267312],
        ['2010', 'Asian or Pacific Islander', 115.0, 8091738.0, 1.421202713],
        ['2010', 'Black or African American', 706.0, 18627343.0, 3.790127234],
        ['2010', 'White', 4340.0, 97061504.0, 4.471391665],
        ['2011', 'American Indian or Alaska Native', 291.0, 2004453.0, 14.517676394],
        ['2011', 'Asian or Pacific Islander', 101.0, 8233348.0, 1.226718463],
        ['2011', 'Black or African American', 664.0, 18795912.0, 3.532683064],
        ['2011', 'White', 4280.0, 97182614.0, 4.404079931],
        ['2012', 'American Indian or Alaska Native', 300.0, 2022565.0, 14.832650619],
        ['2012', 'Asian or Pacific Islander', 94.0, 8515268.0, 1.10389949],
        ['2012', 'Black or African American', 667.0, 18996034.0, 3.511259245],
        ['2012', 'White', 4400.0, 97235779.0, 4.525083303],
        ['2013', 'American Indian or Alaska Native', 314.0, 2041476.0, 15.381028236],
        ['2013', 'Asian or Pacific Islander', 129.0, 8712185.0, 1.480684811],
        ['2013', 'Black or African American', 736.0, 19172832.0, 3.838765186],
        ['2013', 'White', 4448.0, 97325186.0, 4.570245568],
        ['2014', 'American Indian or Alaska Native', 316.0, 2061212.0, 15.330785965],
        ['2014', 'Asian or Pacific Islander', 117.0, 9045827.0, 1.293414079],
        ['2014', 'Black or African American', 655.0, 19437379.0, 3.369795897],
        ['2014', 'White', 4648.0, 97465040.0, 4.76888944],
        ['2015', 'American Indian or Alaska Native', 356.0, 2077645.0, 17.134784817],
        ['2015', 'Asian or Pacific Islander', 139.0, 9351750.0, 1.486352822],
        ['2015', 'Black or African American', 700.0, 19645268.0, 3.563199036],
        ['2015', 'White', 5050.0, 97500538.0, 5.1794586],
        ['2016', 'American Indian or Alaska Native', 364.0, 2091643.0, 17.402587344],
        ['2016', 'Asian or Pacific Islander', 143.0, 9479493.0, 1.508519496],
        ['2016', 'Black or African American', 738.0, 19775471.0, 3.731895943],
        ['2016', 'White', 5106.0, 97311819.0, 5.247050207],
        ['2017', 'American Indian or Alaska Native', 375.0, 2111159.0, 17.762754961],
        ['2017', 'Asian or Pacific Islander', 177.0, 9789167.0, 1.808121161],
        ['2017', 'Black or African American', 707.0, 19993585.0, 3.536134215],
        ['2017', 'White', 5170.0, 97574426.0, 5.298519512],
        ['2018', 'American Indian or Alaska Native', 408.0, 2126784.0, 19.183894556],
        ['2018', 'Asian or Pacific Islander', 164.0, 9953048.0, 1.647736452],
        ['2018', 'Black or African American', 742.0, 20132411.0, 3.685599305],
        ['2018', 'White', 5371.0, 97734219.0, 5.495516366]]
        self.assertEqual(response.as_2d_list(), expected_result)

    def test_as_dataframe(self):
        response = wonder.Response(ResponseFormattingTests.sample_xml, ["Year", "Race"])
        expected_result = """    Year                              Race  Deaths  Population  Crude Rate Per 100,000
0   1999  American Indian or Alaska Native   210.0   1375207.0               15.270428
1   1999         Asian or Pacific Islander    73.0   5813970.0                1.255596
2   1999         Black or African American  1176.0  17026405.0                6.906919
3   1999                             White  5067.0  99715532.0                5.081455
4   2000  American Indian or Alaska Native   213.0   1438695.0               14.805084
..   ...                               ...     ...         ...                     ...
75  2017                             White  5170.0  97574426.0                5.298520
76  2018  American Indian or Alaska Native   408.0   2126784.0               19.183895
77  2018         Asian or Pacific Islander   164.0   9953048.0                1.647736
78  2018         Black or African American   742.0  20132411.0                3.685599
79  2018                             White  5371.0  97734219.0                5.495516

[80 rows x 5 columns]"""
        
        self.assertEquals(str(response), expected_result)
        