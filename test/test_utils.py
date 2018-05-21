import unittest
import ephem
from datetime import datetime
from tracker import utils


class TestGrid(unittest.TestCase):
    def test_valid_grid(self):
        valid_grid = utils.valid_grid

        self.assertTrue(valid_grid('EL'))
        self.assertTrue(valid_grid('EL98'))
        self.assertTrue(valid_grid('EL98qo'))

        self.assertFalse(valid_grid('123456'))
        self.assertFalse(valid_grid('abcdef'))


    def test_grid_to_latlon(self):
        grid_to_latlon = utils.grid_to_latlon

        lat, lon = grid_to_latlon('EL98qo')
        self.assertAlmostEqual(lat, 28.584, 2)
        self.assertAlmostEqual(lon, -80.666, 2) 

    def test_latlon_to_grid(self):
        latlon_to_grid = utils.latlon_to_grid

        self.assertEqual(latlon_to_grid(28.584, -80.666), 'EL98qo')


class TestTimeFormats(unittest.TestCase):
    def setUp(self):
        self.et = ephem.Date((1969, 7, 20, 20, 18, 0))
        self.dt = datetime(1969, 7, 20, 20, 18, 0)

    def test_dt_to_et(self):
        datetime_to_ephem_time = utils.datetime_to_ephem_time

        self.assertEqual(datetime_to_ephem_time(self.dt), self.et)

    def test_et_to_dt(self):
        ephem_time_to_datetime = utils.ephem_time_to_datetime

        self.assertEqual(ephem_time_to_datetime(self.et), self.dt)

    def test_timestamp(self):
        timestamp = utils.timestamp

        self.assertEqual(timestamp(self.et), '1969-07-20 20:18:00')
