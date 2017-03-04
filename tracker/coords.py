import arrow
import math
from math import sin, cos, radians, degrees

# source: http://celestrak.com/columns/v02n02/

PI = math.pi
TWO_PI = 2*PI
EARTH_RADIUS = 6378.135


def julian_date_of_year(year):
    '''
    returns julian date of a given year
    '''
    year -= 1
    a = int(0.01 * year)
    b = 2 - a + int(0.25 * a)
    return int(365.25 * year) + int(30.6001 * 14) + 1720994.5 + b


def day_of_year(year, month, date):
    '''
    returns number of days since Jan 1 for a given year
    '''
    time_str = '%d-%d-%d' % (year, month, date)
    a = arrow.get(time_str, 'YYYY-M-D')
    return int(a.format('DDDD'))


def julian_date(t):
    '''
    returns julian date for a given point in time
    @param t arrow object to convert to julian
    '''
    jd = julian_date_of_year(t.year) + 0.5
    jd += day_of_year(t.year, t.month, t.day)
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
    return (x, y, z)


def calc_user_look_at(pos_sat, lat, lon, alt, t):
    pos = calc_pos(lat, lon, alt, t)
    rx = pos_sat[0] - pos[0]
    ry = pos_sat[1] - pos[1]
    rz = pos_sat[2] - pos[2]
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

    az = math.atan(-top_e/top_s)
    if top_s > 0:
        az += PI
    if az < 0:
        az += TWO_PI

    rg = (rx*rx + ry*ry + rz*rz)**0.5
    el = math.asin(top_z/rg)
    return (az, el, rg)


def get_phi_0(t=arrow.utcnow()):
    (x, y, z) = calc_pos(0, 0, 0, t)
    return math.atan2(y, x)


def eci_to_latlon(pos, phi_0=0):
    (x, y, z) = pos
    rg = (x*x + y*y + z*z)**0.5
    z = z/rg
    if abs(z) > 1.0:
        z = int(z)

    lat = degrees(math.asin(z))
    lon = degrees(math.atan2(y, x)-phi_0)
    if lon > 180:
        lon -= 360
    elif lon < -180:
        lon += 360
    return (lat, lon)


if __name__ == '__main__':
    now = arrow.utcnow()
    lat = 90
    lon = -100
    trd = calc_pos(radians(lat), radians(lon), 0, now)

    phi_0 = get_phi_0()

    z = trd[2]
    r = EARTH_RADIUS
    print(eci_to_latlon(trd, phi_0))
