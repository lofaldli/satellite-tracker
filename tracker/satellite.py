import arrow
import coords
from database import TLEDatabase
from math import radians, degrees

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv


class Satellite:
    def __init__(self, tle):
        (title_line, line_1, line_2) = tle.lines

        self.name = title_line
        self.rv = twoline2rv(line_1, line_2, wgs72)

        self.vel = None
        self.pos = None

    def get_pos(self):
        return self.pos

    def get_vel(self):
        return self.vel

    def propagate(self, t):
        self.time = t
        rv = self.rv.propagate(t.year, t.month, t.day,
                               t.hour, t.minute, t.second)
        if self.rv.error:
            print(self.rv.error_message)
        (self.pos, self.vel) = rv
        return rv

    def get_latlon(self, phi_0=0):
        return coords.eci_to_latlon(self.pos, phi_0)


if __name__ == '__main__':
    db = TLEDatabase()
    iss = db.find_by_name('iss')
    s = Satellite(iss)
    now = arrow.utcnow()
    s.propagate(now)
    phi_0 = coords.get_phi_0(now)
    print(s.get_latlon(phi_0))

    lat = radians(63)
    lon = radians(10)
    alt = 0

    trd = coords.calc_pos(lat, lon, alt, now)
    (az, el, rg) = coords.calc_user_look_at(s.get_pos(), lat, lon, alt, now)
    print(degrees(az), degrees(el), rg)
    print(trd)
