import math
import ephem
from datetime import datetime

import utils

class Satellite(object):
    def __init__(self, tle):
        self.name, self.line1, self.line2 = tle.split('\n')
        self._obj = ephem.readtle(self.name, self.line1, self.line2)

    def compute(self, obs):
        self._obj.compute(obs)

    def propagate(self, obs, delta=ephem.minute):
        obs.date += delta
        self.compute(obs)

    @property
    def azimuth(self):
        return math.degrees(self._obj.az)

    @property
    def elevation(self):
        return math.degrees(self._obj.alt)

    @property
    def latitude(self):
        return math.degrees(self._obj.sublat)

    @property
    def longitude(self):
        return math.degrees(self._obj.sublong)

    def __repr__(self):
        return 'Satellite(name="%s")' % self.name.strip()


class Observer(ephem.Observer):
    def __init__(self, name='', lat=None, lon=None, alt=0, horizon=0, grid=''):
        super().__init__()
        if lat is None or lon is None:
            if grid:
                lat, lon = utils.grid_to_latlon(grid)
            else:
                lat = lon = 0
        self.name, self.lat, self.lon, self.elevation, self.horizon = (
                name, math.radians(lat), math.radians(lon), alt, str(horizon))
        self.grid = utils.latlon_to_grid(lat, lon)

    def next_pass(self, sat, t0=None):
        if t0:
            self.set_date(t0)
        pass_info = super().next_pass(sat._obj)
        pass_ = Pass(pass_info, self, sat)
        self.date = pass_.los + ephem.minute
        return pass_

    def set_date(self, dt):
        self.date = utils.datetime_to_ephem_time(dt)

    def __repr__(self):
        return 'Observer(name="%s", grid="%s")' % (self.name, self.grid)


class Pass(object):
    def __init__(self, info, observer, satellite):
        (self.aos, self.aos_az, self.tca, 
         self.max_el, self.los, self.los_az) = info
        if self.aos > self.los:  # we are in the middle of a pass
            self.aos = self.calc_aos()
        self.observer, self.satellite = observer, satellite

    def calc_aos(self):
        old_date = self.observer.date
        self.observer.date = self.los - 10*ephem.second
        while True:
            # roll back until satellite is below horizon
            self.satellite.propagate(self.observer, -ephem.minute*0.5)
            if satellite.elevation < 0:
                aos = self.observer.date
                break
        self.observer.date = old_date
        self.aos = aos


    def sky_track(self, delta=ephem.minute*0.5):
        coords = []
        self.observer.date = self.aos - delta
        while self.observer.date < self.los:
            self.satellite.propagate(self.observer, delta)
            coords.append((self.satellite.azimuth, self.satellite.elevation))
        return coords


    def __str__(self):
        return '%s | %5.1f | %s | %5.1f | %s | %5.1f' % (
                utils.timestamp(self.aos), math.degrees(self.aos_az), 
                utils.timestamp(self.tca), math.degrees(self.max_el),
                utils.timestamp(self.los), math.degrees(self.los_az))

    def __repr__(self):
        return 'Pass(aos="%s", los="%s")' % (utils.timestamp(self.aos), 
                                             utils.timestamp(self.los))

    @property
    def duration(self):
        return utils.delta_t(self.aos, self.los)

if __name__ == '__main__':
    esoc = Observer('ESOC', grid='JN49hu')
    iss = Satellite('''\
ISS (ZARYA)             
1 25544U 98067A   18038.58038997  .00002133  00000-0  39542-4 0  9995
2 25544  51.6420 304.8284 0003298  83.0669 341.5168 15.54068423 98365''')
    esoc.set_date(datetime.now())
    iss.propagate(esoc)
    print(esoc.next_pass(iss))
