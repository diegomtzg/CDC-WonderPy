import cdcwonderpy as wonder
import unittest
import math
import bs4 as bs
import pandas as pd

# Testing parsing of response
class RequestInternalTest(unittest.TestCase):
    def test_icd10_methods(cls):
    	assert(math.isclose(ICD10Code._convert_to_numeric(ICD10Code.A00.value), 0.0))
    	assert(math.isclose(ICD10Code._convert_to_numeric(ICD10Code.A16.value), 16.0))
    	assert(math.isclose(ICD10Code._convert_to_numeric(ICD10Code.A16_2.value), 16.2))
    	assert(math.isclose(ICD10Code._convert_to_numeric(ICD10Code.B08_2.value), 108.2))
    	assert(ICD10Code.contains(ICD10Code.L80_L98, ICD10Code.L98_9))
    	assert(ICD10Code.contains(ICD10Code.Y70_Y82, ICD10Code.Y73))
    	assert(ICD10Code.contains(ICD10Code.Y89, ICD10Code.Y89))
    	assert(not ICD10Code.contains(ICD10Code.Y84_0, ICD10Code.Y83_Y84))