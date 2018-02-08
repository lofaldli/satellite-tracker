import time
import ephem
from ui import UI
from database import find_by_id
from models import Satellite, Observer, Pass


def list_passes(obs, sat, n=10):
    i = 0
    while i < n:
        p = obs.next_pass(sat)
        obs.date = p.los + ephem.minute
        if p.los < p.aos:
            continue
        if p.max_el < obs.horizon:
            continue
        print(p)
        i += 1


def live_tracking(obs, sats, interactive=True):
    if interactive:
        ui = UI()
    while True:
        try:
            lines = [
                str(obs), 
                'SATELLITE                AZ     EL     LAT     LON', 
                '-----------------------------------------------------',
            ]
            obs.date = ephem.now()
            for sat in sats:
                sat.compute(obs)
                lines.append(str(sat))

            if interactive:
                ui.update(lines)
            else:
                print('\n'.join(lines))
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    obs = Observer('ESOC', grid='JN49hu', alt=135, horizon=5.0)
    sats = (Satellite(find_by_id(25544)),
            Satellite(find_by_id(24278)),
            Satellite(find_by_id(35932)),
    )

    live_tracking(obs, sats, True)
    #list_passes(obs, sats[0])
