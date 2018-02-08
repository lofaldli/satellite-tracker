import ephem
from math import degrees, radians
from utils import latlon_to_grid, grid_to_latlon, timestamp, delta_t

class Satellite(object):
    def __init__(self, tle):
        self.name, self.line1, self.line2 = tle.split('\n')
        self.obj = ephem.readtle(self.name, self.line1, self.line2)

    def compute(self, obs):
        self.obj.compute(obs)

    def __str__(self):
        return '%s %6.2f %6.2f %6.2f %7.2f' % (
                self.name.ljust(24), 
                degrees(self.obj.az), degrees(self.obj.alt),
                degrees(self.obj.sublat), degrees(self.obj.sublong))

    def __repr__(self):
        return 'Satellite(name="%s")' % self.name.strip()


class Observer(ephem.Observer):
    def __init__(self, name='', lat=None, lon=None, alt=0, horizon=0, grid=''):
        super().__init__()
        if lat is None or lon is None:
            if grid:
                lat, lon = grid_to_latlon(grid)
            else:
                lat = lon = 0
        self.name, self.lat, self.lon, self.elevation, self.horizon = (
                name, radians(lat), radians(lon), alt, str(horizon))
        self.grid = latlon_to_grid(lat, lon)

    def next_pass(self, sat):
        return Pass(super().next_pass(sat.obj))

    def __str__(self):
        return '%s (%.2fN, %.2fE)' % (
                self.name, degrees(self.lat), degrees(self.lon))

    def __repr__(self):
        return 'Observer(name="%s", grid="%s")' % (self.name, self.grid)


class Pass:
    def __init__(self, info):
        (self.aos, self.aos_az, self.tca, 
         self.max_el, self.los, self.los_az) = info

    def __str__(self):
        return '%s | %5.1f | %s | %5.1f | %s | %5.1f' % (
                timestamp(self.aos), degrees(self.aos_az), 
                timestamp(self.tca), degrees(self.max_el),
                timestamp(self.los), degrees(self.los_az))

    def __repr__(self):
        return 'Pass(aos="%s", los="%s")' % (timestamp(self.aos), 
                                             timestamp(self.los))

    @property
    def duration(self):
        return delta_t(self.aos, self.los)

if __name__ == '__main__':
    esoc = Observer('ESOC', grid='JN49hu')
    iss = Satellite('''\
ISS (ZARYA)             
1 25544U 98067A   18038.58038997  .00002133  00000-0  39542-4 0  9995
2 25544  51.6420 304.8284 0003298  83.0669 341.5168 15.54068423 98365''')
    p = esoc.next_pass(iss)
    print(repr(esoc))
    print(repr(iss))
    print(repr(p))
    print(p.duration)
