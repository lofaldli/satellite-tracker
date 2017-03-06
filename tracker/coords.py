import arrow
from collections import namedtuple
from math import pi, radians, degrees, sin, cos, asin, atan, atan2

# source: http://celestrak.com/columns/v02n02/

TWO_PI = 2*pi
EARTH_RADIUS = 6378.135

Position = namedtuple('Position', ['x', 'y', 'z'])
LatLon = namedtuple('LatLon', ['lat', 'lon'])


def jdoy(year):
    '''
    julian day of Jan 1 for a given year
    '''
    year -= 1
    a = int(0.01 * year)
    b = 2 - a + int(0.25 * a)
    return int(365.25 * year) + int(30.6001 * 14) + 1720994.5 + b


def doy(year, month, date):
    '''
    day of year
    '''
    time_str = '%d-%d-%d' % (year, month, date)
    a = arrow.get(time_str, 'YYYY-M-D')
    return int(a.format('DDDD'))


def julian_date(t):
    '''
    returns julian date for a given point in time
    '''
    jd = jdoy(t.year) + 0.5
    jd += doy(t.year, t.month, t.day)
    jd += (1.0 * t.hour - 12) / 24 + \
          (1.0 * t.minute) / 1440 +  \
          (1.0 * t.second) / 86400

    return jd


def theta_g_JD(jd):
    '''
    returns theta_g for a given julian date
    '''
    UT = jd + 0.5
    UT -= int(UT)
    jd = jd - UT
    TU = (jd - 2451545.0)/36525
    GMST = 24110.54841 + TU * (8640184.812866 + TU * (0.093104 - TU * 6.2e-6))
    GMST = (GMST + 86400.0*1.00273790934*UT) % 86400.0
    return TWO_PI * GMST / 86400.0


def calc_pos(lat, lon, alt, t):
    '''
    returns eci position for a given lat, lon, alt and time
    '''
    jd = julian_date(t)
    theta = (theta_g_JD(jd) + lon) % TWO_PI
    r = (EARTH_RADIUS + alt)

    x = r * cos(theta) * cos(lat)
    y = r * sin(theta) * cos(lat)
    z = r * sin(lat)
    return Position(x, y, z)


def calc_user_look_at(pos_sat, lat, lon, alt, t):
    pos = calc_pos(lat, lon, alt, t)
    rx = pos_sat.x - pos.x
    ry = pos_sat.y - pos.y
    rz = pos_sat.z - pos.z
    jd = julian_date(t)
    theta = (theta_g_JD(jd) + lon) % TWO_PI

    top_s = sin(lat) * cos(theta) * rx +  \
        sin(lat) * sin(theta) * ry -  \
        cos(lat) * rz
    top_e = -sin(theta) * rx + \
        cos(theta) * ry
    top_z = cos(lat) * cos(theta) * rx +  \
        cos(lat) * sin(theta) * ry +  \
        sin(lat) * rz

    az = atan(-top_e/top_s)
    if top_s > 0:
        az += pi
    if az < 0:
        az += TWO_PI

    rg = (rx*rx + ry*ry + rz*rz)**0.5
    el = asin(top_z/rg)
    return (az, el, rg)


def phi0(t):
    (x, y, z) = calc_pos(0, 0, 0, t)
    return atan2(y, x)


def eci_to_latlon(pos, phi_0=0):
    (x, y, z) = pos
    rg = (x*x + y*y + z*z)**0.5
    z = z/rg
    if abs(z) > 1.0:
        z = int(z)

    lat = degrees(asin(z))
    lon = degrees(atan2(y, x)-phi_0)
    if lon > 180:
        lon -= 360
    elif lon < -180:
        lon += 360
    assert -90 <= lat <= 90
    assert -180 <= lon <= 180
    return lat, lon


def latlon2uv(latlon):
    lat, lon = latlon
    assert -90 <= lat <= 90
    assert -180 <= lon <= 180

    u = (lon + 180) / 360
    v = (90 - lat) / 180
    assert 0 <= u <= 1
    assert 0 <= v <= 1

    return u, v

if __name__ == '__main__':
    now = arrow.utcnow()
    lat = 90
    lon = -100
    trd = calc_pos(radians(lat), radians(lon), 0, now)

    phi_0 = phi0(arrow.utcnow())

    z = trd[2]
    r = EARTH_RADIUS
    print(eci_to_latlon(trd, phi_0))
