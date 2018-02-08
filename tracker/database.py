import atexit
import sqlite3
import requests

conn = sqlite3.connect('tles.db')
atexit.register(conn.close)

SOURCES = (
        'http://www.amsat.org/amsat/ftp/keps/current/nasabare.txt',
        'https://celestrak.com/NORAD/elements/stations.txt',
        'https://celestrak.com/NORAD/elements/amateur.txt',
        'https://celestrak.com/NORAD/elements/cubesat.txt',
)

def init_db():
    '''initialize database table'''
    conn.cursor().execute('''create table if not exists tles (
            id integer primary key unique, tle text)''')
    conn.commit()

def insert(lines):
    '''insert lines into database'''
    rows = make_rows(lines)
    c = conn.cursor()
    c.executemany('insert or replace into tles values (?,?)', rows)
    conn.commit()

def norad_id(tle):
    '''get norad id from tle'''
    return int(tle.split('\n')[1][2:7])

def make_rows(lines):
    '''turn tle file into database rows'''
    rows = []
    for i in range(0, len(lines), 3):
        if i+3 > len(lines):
            break
        tle = '\n'.join(lines[i:i+3])
        id = norad_id(tle)
        rows.append((id, tle))
    return rows

def read_tles(filename):
    '''read lines from file containing tles'''
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return lines

def get(url):
    '''get content from url'''
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        print(url, r.status_code)

def fetch_tles(url):
    '''fetch lines from website lines'''
    data = get(url)
    lines = data.splitlines()
    return lines

def update_from_network():
    init_db()
    for source in SOURCES:
        rows = fetch_tles(source)
        insert(rows)

def find_by_id(id):
    '''return tle of row matcing norad id'''
    c = conn.cursor()
    c.execute('select * from tles where id=(?)', (id,))
    res = c.fetchone()
    if res:
        id, tle = res
        return tle

if __name__ == '__main__':
    update_from_network()
    print(find_by_id(25544))
