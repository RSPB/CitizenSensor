from unittest import TestCase
import gps

class Test_GPS(TestCase):

    def test_convert_to_deg(self):
        res = gps.convert_to_deg(51, 9, 45.9)
        self.assertAlmostEqual(res, 51.16275, 5)

    def test_rational_to_real(self):
        res = gps.rational_to_real(42, 5)
        self.assertEquals(res, 8.4)

    def test_get_gps_metadata_no_location(self):
        res = gps.get_gps_metadata('test/27302080E.jpg')
        self.assertEquals(len(res), 4)
        self.assertEquals(res['altitude'], 774)
        self.assertEquals(res['date'], '2012-05-18')
        self.assertEquals(res['datum'], 'WGS-84')
        position = (round(res['position'][0], 6), round(res['position'][1], 6))
        self.assertEquals(position, (40.031789, 8.757676))

    def test_get_gps_metadata_with_location(self):
        res = gps.get_gps_metadata('test/27302080E.jpg', reverse_location=True)
        self.assertEquals(len(res), 5)
        self.assertEquals(res['location'], u'Vecchia Strada Comunale Zerfaliu-Paulilatino, Paulle/Paulilatino, OR, SAR, 09070, Italia',
                          "Translation of coordinates to location's name failed. Test is expected to fail if there is "
                           "no internet connection")
