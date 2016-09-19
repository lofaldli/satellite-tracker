import re
import arrow

def norm(string):
    # -00123-4 -> -.00123e-4
    return float(string[0] + '.' + string[1:6] + 'e' + string[6:])

def checksum(line):
    line, n = re.subn('-', '1', line)    # replace dashes with 1's
    line, n = re.subn('[^\d]', '', line) # remove non-digit chars
    # compare with last digit with sum modulo 10
    digits = [int(x) for x in line[:-1]]
    return int(line[-1]) == sum(digits) % 10

class TLE:
    def __init__(self, tle_string):
        '''
        @param tle_string should be a single string containing three lines
        '''
        (title_line, line_1, line_2) = (self.lines) = tle_string.split('\n')

        self.parse_title_line(title_line)
        self.parse_line_1(line_1)
        self.parse_line_2(line_2)

        if not checksum(line_1):
            print 'invalid checksum in line 1 of %s #%d' % (self.sat_name, self.set_no)
        if not checksum(line_2):
            print 'invalid checksum in line 2 of %s #%d' % (self.sat_name, self.set_no)

    def parse_title_line(self, line):
        self.sat_name = line[0:24]

    def parse_line_1(self, line):
        self.sat_num        = int(line[2:7])     # satellite number
        self.classification = line[7]            # classification (U=unclassified)
        self.launch_year    = int(line[9:11])    # international designator - launch year (last two digits)
        self.launch_no      = int(line[11:14])   # international designator - launch number of the year
        self.launch_piece   = line[14:17]        # international designator - piece of the launch
        self.epoch_year     = line[18:20]        # epoch year (last two digits)
        self.epoch_day      = float(line[20:32]) # epoch (day of the year and fractional portion of the day)
        self.ftdmm2         = float(line[33:43]) # first time derivative of mean motion divided by two
        self.stdmm6         = norm(line[44:52])  # second time derivative of mean motion divided by six
        self.bstar_drag     = norm(line[53:61])  # BSTAR drag term
        _                   = int(line[62])      # the number zero
        self.set_no         = int(line[64:68])   # element set number
        _                   = int(line[68])      # checksum


    def parse_line_2(self, line):
        _                 = int(line[2:7])         # satellite number
        self.incl         = float(line[8:16])      # inclination (degrees)
        self.r_asc        = float(line[17:25])     # right ascension of the ascending node (degrees)
        self.ecc          = float('.'+line[26:33]) # eccentricity
        self.arg_p        = float(line[34:42])     # argument of perigee (degrees)
        self.m_anom       = float(line[43:51])     # mean anomaly (degrees)
        self.mm           = float(line[52:63])     # mean motion (revolutions per day)
        self.rev_at_epoch = int(line[63:68])       # revolution number at epoch
        _                 = int(line[68])          # checksum


    @property
    def epoch(self):
        year = arrow.get(self.epoch_year, 'YY').year
        return arrow.get(self.epoch_day * 86400).replace(year=year)





if __name__=='__main__':

    iss ='''ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537'''

    t = TLE(iss)
    print t.epoch


