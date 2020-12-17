import cdcwonderpy as wonder
from cdcwonderpy.icd10code import *
import unittest
import math
import bs4 as bs
import pandas as pd
import re

def parse_as_int(xml):
    return 7

# Testing parsing of response
class RequestInternalTest(unittest.TestCase):
    def test_icd10_methods(cls):
        assert(math.isclose(ICD10Code.A00._convert_to_numeric()[0], 0.0))
        assert(math.isclose(ICD10Code.A16._convert_to_numeric()[0], 16.0))
        assert(math.isclose(ICD10Code.A16._convert_to_numeric()[1], 16.9))
        assert(math.isclose(ICD10Code.A16_2._convert_to_numeric()[0], 16.2))
        assert(math.isclose(ICD10Code.B08_2._convert_to_numeric()[0], 108.2))
        assert(ICD10Code.L80_L98.contains(ICD10Code.L98_9))
        assert(ICD10Code.Y70_Y82.contains(ICD10Code.Y73))
        assert(ICD10Code.Y89.contains(ICD10Code.Y89))
        assert(not ICD10Code.Y84_0.contains(ICD10Code.Y83_Y84))
        assert(ICD10Code.description_best_match("Diseases of the nervous system") == ICD10Code.G00_G98)
        assert(ICD10Code.description(ICD10Code.G00_G98) == "Diseases of the nervous system")
        assert((len(ICD10Code.description_matches_above_threshold("Kidney"))) == 44)
        assert(len(ICD10Code.description_matches_regex("disease.*( ear(\W+|$)| throat(\W+|$))", re.I)) == 7)

    def test_response_obj_custom(cls):
        resp = wonder.Response("HI YASS QUEEN", None)
        assert(resp.as_custom(parse_as_int) == 7)