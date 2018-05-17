import re
import ephem
from datetime import datetime, timedelta

def valid_grid(grid):
    mo = re.match(r'^[A-R]{2}([0-9]{2}([a-x]{2})?)?$', grid, re.IGNORECASE)
    return mo is not None

def grid_to_latlon(grid):
    if not valid_grid(grid):
        raise Exception('invalid grid locator %s' % grid)
    grid = grid.lower()
    lat, lon = -90.0, -180.0

    lon += 20*(ord(grid[0]) - ord('a'))
    lat += 10*(ord(grid[1]) - ord('a'))
    if len(grid) == 2:
        return lat, lon

    lon += 2*int(grid[2])
    lat += 1*int(grid[3])
    if len(grid) == 4:
        return lat, lon

    lon += (2/24) * (ord(grid[4]) - ord('a'))
    lat += (1/24) * (ord(grid[5]) - ord('a'))

    return lat, lon

def latlon_to_grid(lat, lon, precision=2):
    grid = ''

    grid += chr(int((lon + 180.0)/20) + ord('A'))
    grid += chr(int((lat + 90.0)/10) + ord('A'))
    if precision == 0:
        return grid

    grid += str(int(lon % 20 / 2))
    grid += str(int(lat % 10))
    if precision == 1:
        return grid

    grid += chr(int(lon % 2 * 12) + ord('a'))
    grid += chr(int(lat % 1 * 24) + ord('a'))
    return grid

def ephem_time_to_datetime(et):
    return datetime(*map(int, et.tuple()))

def datetime_to_ephem_time(dt):
    return ephem.Date((dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))

def timestamp(et, fmt='%Y-%m-%d %H:%M:%S'):
    return ephem_time_to_datetime(et).strftime(fmt)

def delta_t(t0, t1):
    return ephem_time_to_datetime(t1) - ephem_time_to_datetime(t0)


if __name__ == '__main__':
    #print(grid_to_latlon('AA00aa'))
    #print(grid_to_latlon('JN49hu'))

    print(latlon_to_grid(49.85, 8.62, 0))
    print(latlon_to_grid(49.85, 8.62, 1))
    print(latlon_to_grid(49.85, 8.62, 2))
