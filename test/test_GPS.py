from unittest import TestCase
from nose.tools import assert_equals
import gps

class Test_GPS(TestCase):

    def test_convert_to_deg(self):
        res = gps.convert_to_deg(51, 9, 45.9)
        assert_equals(round(res, 5), 51.16275)

    def test_rational_to_real(self):
        res = gps.rational_to_real(42, 5)
        assert_equals(res, 8.4)

    def test_get_gps_metadata_no_location(self):
        res = gps.get_gps_metadata('test/27302080E.jpg')
        assert_equals(len(res), 4)
        assert_equals(res['altitude'], 774)
        assert_equals(res['date'], '2012-05-18')
        assert_equals(res['datum'], 'WGS-84')
        position = (round(res['position'][0], 6), round(res['position'][1], 6))
        assert_equals(position, (40.031789, 8.757676))

    def test_get_gps_metadata_with_location(self):
        res = gps.get_gps_metadata('test/27302080E.jpg', reverse_location=True)
        assert_equals(len(res), 5)
        assert_equals(res['location'], u'Vecchia Strada Comunale Zerfaliu-Paulilatino, Paulle/Paulilatino, OR, SAR, 09070, Italia',
                      "Translation of coordinates to location's name failed. Test is expected to fail if there is "
                      "no internet connection")
