"""
    The SunEquation class is used approximately calculate the sunset and
    sunrise times using the Sunrise Equation found on Wikipedia.
"""

import math
import logging
# from datetime import datetime, timezone
import datetime
import pytz
from tzlocal import get_localzone


class SunEquation:
    """
        Used to calculate sunrise and sunset time for the current day.
        Using the full sunrise equation as found on Wikipedia.
        https://en.wikipedia.org/wiki/Sunrise_equation
        The sunrise and sunset times obtained are accurate to within 5
        minutes. #FUTURE: test the accuracy of this theory.
    """

    def __init__(self, latitude, longitude):
        self.date_today = datetime.date.today()
        self.longitude_west = longitude
        self.latitude = latitude
        self.jdn = None
        self.rise = None
        self.set = None
        self.timezone = None

    def calculate(self):
        """
            Calculate sunrise and sunset datetime objects based upon
            the Wikipedia Sunrise Equation formuale
        """
        logging.debug("New day, new calculations")
        n = self.current_julian_day()
        j_star = self.mean_solar_moon(n, self.longitude_west)
        m = self.solar_mean_anomaly(j_star)
        c = self.equation_of_the_centre(m)
        lam = self.ecliptic_longitude(m, c)
        j_transit = self.solar_transit(j_star, m, lam)
        theta = self.declination_of_the_sun(lam)
        w_o = self.hour_angle(self.latitude, theta)
        self.suntimes(j_transit, w_o)
        return self.rise, self.set

    def current_julian_day(self):
        """
            Calculates the current julian calandar day.
            Equation:
            n = j_date - 2451545.5 + 0.0008
        """
        # fmt = '%Y.%m.%d'
        # s = '2012.11.07'
        # dt = datetime.datetime.strptime
        jdn = self.julian_date(
            self.date_today.year,
            self.date_today.month,
            self.date_today.day)
        n = jdn - 2451545.0 + 0.0008
        logging.debug("Current julain day %s", str(n))
        return n

    def julian_date(self, year, month, day):
        """
            Returns Julian date according to:
        """
        self.jdn = ((1461*(year+4800+(month-14)/12))/4
                    + (367*(month-2-12*((month-14)/12)))/12
                    - (3*((year+4900+(month-14)/12)/100))/4
                    + day - 32075)
        logging.debug("Julian day calculated: %s", str(self.jdn))
        return self.jdn

    def mean_solar_moon(self, n, longitude_west):
        """
            Calculates the mean solar moon,
            n = number of days since 1st Jan 2000 from julian_day() output
            longitude_west = longitude of an observer on earth with west
            negative and east positive.
        """
        j_star = n - (longitude_west/360)
        logging.debug("Mean solar moon: %s", str(j_star))
        return j_star

    def solar_mean_anomaly(self, j_star):
        """
            Calculates the solar mean anomaly dependent on the j* value
            from mean_solar_moon()
            j* = mean solar moon
        """
        m = (357.5291 + 0.98560028 * j_star) % 360
        logging.debug("Solar mean anaomly: %s", str(m))
        return m

    def equation_of_the_centre(self, m):
        """
            Calculates the Equation of the center
        """
        c = 1.9148*math.sin(math.radians(m))  \
            + 0.0200*math.sin(math.radians(2*m)) \
            + 0.0003*math.sin(math.radians(3*m))
        logging.debug("Equation of the center: %s", str(c))
        return c

    def ecliptic_longitude(self, m, c):
        """
            Calculates the lambda from the ecliptic longitude
        """
        lam = (m + c + 180 + 102.9372) % 360
        logging.debug("Ecliptic longitude: %s", str(lam))
        return lam

    def solar_transit(self, j_star, m, lam):
        """
            Calculates the solar transient.
        """
        j_transit = 2451545.5 + j_star \
                    + 0.0053*math.sin(math.radians(m)) \
                    - 0.0069*math.sin(math.radians(2*lam))
        logging.debug("Solar transient: %s", str(j_transit))
        return j_transit

    def declination_of_the_sun(self, lam):
        """
            Calculates the declination of the sun.
        """
        theta = math.degrees(
            math.asin(
                math.sin(math.radians(lam))
                * math.sin(math.radians(23.44))))
        # theta = degrees(asin(sin(radians(lam))*(sin(radians(23.44)))
        logging.debug("Declination of the Sun: %s", str(theta))
        return theta

    def hour_angle(self, latitude, theta, a=0):
        """
            Calculates the Hour angle.
        """
        w_o = math.degrees(
            math.acos(
                (math.sin(
                    math.radians(-0.83+a)
                    - math.sin(math.radians(latitude))
                    * math.sin(math.radians(theta)))
                 / (math.cos(
                     math.radians(latitude))
                    * math.cos(math.radians(theta))))))
        logging.debug("Hour angle: %s", str(w_o))
        return w_o

    def suntimes(self, j_transit, w_o):
        """
            Calculates sunrise time.
        """
        j_rise = j_transit - w_o/360
        j_set = j_transit + w_o/360
        t_rise = j_rise - self.jdn
        t_set = j_set - self.jdn
        logging.debug("Rise")
        rise_temp = self.julian_to_timedelta(t_rise)
        logging.debug("Set")
        set_temp = self.julian_to_timedelta(t_set)
        tz = get_localzone() #Need to replace to reduce dependency by 1
        today = datetime.datetime(
            datetime.date.today().year,
            datetime.date.today().month,
            datetime.date.today().day,
            hour=0,
            tzinfo=pytz.timezone('UTC')
        )
        self.rise = rise_temp + today
        self.set = set_temp + today
        self.rise = self.rise.astimezone(tz)
        self.set = self.set.astimezone(tz)
        self.timezone = tz
        logging.debug("Sunrise: %s", self.rise.strftime("%d/%m/%y %H:%M %p  %Z"))
        logging.debug("Sunrise: %s", self.set.strftime("%d/%m/%y %H:%M %p  %Z"))

    def julian_to_timedelta(self, julian):
        """
            Takes a fraction of a julain day and returns the time as a
            datetime element.
        """
        assert julian < 1
        hour = math.floor(julian*24)
        minute = math.floor((julian*24-hour)*60)
        delta = datetime.timedelta(hours=hour, minutes=minute)
        logging.debug("Time Delta: %s", str(delta))
        return delta

    def format_yaml(self):
        """
            Writes date, sunrise and sunset times to a dictionary
            following ISO standards. This data can then be written to a
            file.
        """
        today = datetime.date.today().isoformat()
        rise = self.rise.isoformat()
        fall = self.set.isoformat()
        timezone = self.rise.tzinfo.zone
        """
            This is a workaround. Tied to using get_localzone in
            suntimes(). Gathering the current timezone some other way
            will reduce this dependency.
        """
        output = {
            "date": today,
            "sunrise": rise,
            "sunset": fall,
            "timezone": timezone,
        }
        return output
