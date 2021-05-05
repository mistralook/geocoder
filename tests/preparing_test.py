import unittest
import sqlite3
import os
from parse_script import Parser


class PreparingBaseTest(unittest.TestCase):
    cb = 'parsed_data_test.db'

    def setUp(self, current_base=cb):
        osm_base = 'rutland.osm'
        Parser(current_base).run(osm_base)

    def test_preprocessing(self, current_base=cb):
        s = "SELECT lat, lon FROM WayBuildings"
        prepared_base = 'beforehead_prepared_base.db'
        r1 = sqlite3.connect(prepared_base).cursor().execute(s).fetchall()
        r2 = sqlite3.connect(current_base).cursor().execute(s).fetchall()
        self.assertEqual(r1, r2)

    def test_known_address(self, current_base=cb):
        first_addr = [('South Street', '96')]
        s = f"SELECT street, housenumber FROM WayBuildings" \
            f" WHERE street='{first_addr[0][0]}'" \
            f" AND housenumber='{first_addr[0][1]}'"
        r1 = sqlite3.connect(current_base).cursor().execute(s).fetchall()
        self.assertEqual(first_addr, r1)

    def test_known_address_two(self, current_base=cb):
        second_addr = [('High Street', '64')]
        s = f"SELECT street, housenumber FROM WayBuildings" \
            f" WHERE street='{second_addr[0][0]}'" \
            f" AND housenumber='{second_addr[0][1]}'"
        r2 = sqlite3.connect(current_base).cursor().execute(s).fetchall()
        self.assertEqual(second_addr, r2)

    def tearDown(self, current_base=cb):
        os.remove(current_base)


if __name__ == '__main__':
    unittest.main()
