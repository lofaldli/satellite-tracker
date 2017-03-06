import arrow
import coords
from math import pi, cos
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs72


class ViewModel(object):
    def __init__(self, name):
        self.name = name


class SatelliteViewModel(ViewModel):
    def __init__(self, name, line1='', line2=''):
        super().__init__(name)
        if line1 and line2:
            self.satelliteObject = twoline2rv(line1, line2, wgs72)
        else:
            self.satelliteObject = None

    def propagate(self, t):
        pos, vel = self.satelliteObject.propagate(t.year, t.month, t.day,
                                                  t.hour, t.minute, t.second)
        if self.satelliteObject.error:
            print(self.satelliteObject.error_message)
            return (0, 0, 0), (0, 0, 0)

        return pos, vel

    def latlon(self, t=None):
        if not t:
            t = arrow.utcnow()
        pos, vel = self.propagate(t)
        lat, lon = coords.eci_to_latlon(pos, coords.phi0(t))
        return coords.LatLon(lat, lon)


class DummySatelliteViewModel(SatelliteViewModel):
    def latlon(self, t=None):
        if not t:
            t = arrow.utcnow()
        t = coords.julian_date(t) * 10000
        lat = 80 * cos(2*pi*t)
        lon = ((100 * t) % 360) - 180
        return lat, lon


class GroundStationViewModel(ViewModel):
    def __init__(self, name, latlon=coords.LatLon(0, 0)):
        super().__init__(name)
        self.latlon_ = latlon

    def latlon(self, t=0):
        return self.latlon_.lat, self.latlon_.lon
