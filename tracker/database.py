import os
import re
import urllib
from tle import TLE

groups = [
    'amateur',
    'galileo',
    'globalstar',
    'noaa',
    'stations',
    'science',
    'weather'
]

URL_FORMAT = 'http://celestrak.com/NORAD/elements/{}.txt'
DATA_PATH = '../data'
LOCAL_FORMAT = os.path.join(DATA_PATH, '{}.txt')


def download_file(group):
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
    remote = URL_FORMAT.format(group)
    local = LOCAL_FORMAT.format(group)
    print('fetching', remote, '=>', local)
    urllib.urlretrieve(remote, local)


def update_all():
    for group in groups:
        download_file(group)


def read_file(group):
    with open(LOCAL_FORMAT.format(group)) as f:
        content = f.read()
    return content


def load_data(group):
    content = read_file(group)
    lines = content.split('\n')

    data = []
    for i in range(0, len(lines), 3):
        if lines[i]:
            tle_lines = '\n'.join(lines[i:i+3])
            data.append(TLE(tle_lines))

    return data


def load_all():
    data = []
    for group in groups:
        data.extend(load_data(group))
    return data


class TLEDatabase:
    def __init__(self, update=True):
        if update:
            update_all()
        self.data = load_all()

    def find_by_name(self, name):
        for d in self.data:
            if re.search(name, d.sat_name, re.IGNORECASE):
                return d

        print('could not find satellite with name %s' % name)
        return None

    def find_all_by_name(self, name):
        rv = []
        for d in self.data:
            if re.search(name, d.sat_name, re.IGNORECASE):
                rv.append(d)

        if not rv:
            print('could not find any satellites with name %s' % name)
        return rv


if __name__ == '__main__':
    # update_all()
    db = TLEDatabase()
    data = db.find_by_name('iss')
    if data:
        print(data.sat_name)
