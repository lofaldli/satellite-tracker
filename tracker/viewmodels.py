import arrow
import coords
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv


class ViewModel(object):
    def __init__(self, name):
        self.name = name


class SatelliteViewModel(ViewModel):
    def __init__(self, name, line1, line2):
        super().__init__(name)
        self.satelliteObject = twoline2rv(line1, line2, wgs72)

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
        return lat, lon


class GroundStationViewModel(ViewModel):
    def __init__(self, name, latlon=coords.LatLon(0, 0)):
        super().__init__(name)
        self.latlon_ = latlon

    def latlon(self, t=0):
        return self.latlon_.lat, self.latlon_.lon
