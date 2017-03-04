import arrow
import coords
from gui import GUI
from database import TLEDatabase
from satellite import Satellite

sats = []


def main():
    db = TLEDatabase()
    tles = []
    tles.append(db.find_by_name('iss'))
    tles.append(db.find_by_name('hst'))
    tles.extend(db.find_all_by_name('globalstar'))
    # tles.extend(db.find_all_by_name('formosat'))
    # tles.extend(db.find_all_by_name('gsat'))

    for t in tles:
        sats.append(Satellite(t))

    gui = GUI()
    gui.set_background('../images/world_map.jpg')
    gui.main_loop(callback, run_once=False)


def callback():
    now = arrow.utcnow()
    phi_0 = coords.get_phi_0(now)
    points = []
    for sat in sats:
        sat.propagate(now)
        lat, lon = sat.get_latlon(phi_0)
        x = (lon + 180.0) / 360.0
        y = (90.0 - lat) / 180.0
        label = sat.name
        points.append(dict(x=x, y=y, label=label))

    return points


if __name__ == '__main__':
    main()
