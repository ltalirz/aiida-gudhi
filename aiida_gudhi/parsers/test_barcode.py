""" Tests for barcode parser

"""
import os
import numpy.testing as npt
import aiida_gudhi.tests as gt
from aiida_gudhi.parsers.barcode import BarcodeParser


class TestBarcode(gt.PluginTestCase):
    def test_parse_hkust_barcode(self):

        max_life = 4.2
        parser = BarcodeParser(
            filename=os.path.join(gt.TEST_DIR, 'sample.barcode'),
            max_life=max_life)

        npt.assert_almost_equal(
            parser.get_life_lines(0)[1], [0, 2.4379], decimal=2)
        npt.assert_almost_equal(
            parser.get_life_lines(1)[1], [4.06, max_life], decimal=2)
        npt.assert_almost_equal(
            parser.get_life_lines(2)[1], [4.02, max_life], decimal=2)
