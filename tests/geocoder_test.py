import unittest
import os
from tests import base_for_geocoder_test
from find_address import find


class SimpleGeocoderTest(unittest.TestCase):
    base = 'isle_of_wight_test.db'

    def setUp(self):
        base_for_geocoder_test.create_base()

    def test_simple_request(self, db=base):
        street = 'Church Street'
        housenumber = '23'
        lat, lon = 50.594149645454536, -1.2070199999999998
        out = find(db, street, housenumber)
        with self.subTest():
            self.assertEqual(out['lat'], lat)
        with self.subTest():
            self.assertEqual(out['lon'], lon)

    def tearDown(self, db=base):
        os.remove(db)


if __name__ == '__main__':
    unittest.main()
