"""The DesktopChanger class is the expected method of interacting with
the functionality provided by this module. Methods that should be 
called by the calling class object:
* updater

TODO: Fill out info of the methods to call to perform specific tasks.
    These methods take into account the config.yaml and command-line 
    options.
"""

import subprocess
from pathlib import Path
import logging
import random
import datetime
import pytz
import iso8601
from desktopchanger.utils import CSVFileIO, yamlFileIO
from desktopchanger.sunequation import SunEquation

sys_random = random.SystemRandom()

##### Functions
#####
def randomiser(wallpapers):
    """ Return a random wallpaper from a list.
    """
    return random.choice(wallpapers)


##### Classes
#####
class DesktopChanger:
    """High level control class.
    """

    def __init__(self, args):
        """ Takes in the command line options and reads the contents
        of the yaml configuration .
        """
        if args.image is not None:
            self.wallpaper_file = Path(str(args.image))
        else:
            self.wallpaper_file = None
        yaml_config = yamlFileIO("", "config.yaml")
        yaml_config.readYaml()
        self.csvfile = yaml_config.data['csvFile']
        self.latitude = yaml_config.data['latitude']
        self.longitude = yaml_config.data['longitude']

    def update_sun(self):
        """Retrieve sun information from file or update the information if the 
        day (TODO: future location) information has changed.
        """
        dates_yaml = yamlFileIO("data", "dates.yaml")
        dates_yaml.readYaml()
        # Read file for date information
        if len(dates_yaml.data) is not 0:
            self.date = iso8601.parse_date(dates_yaml.data['date'])
            if self.date == datetime.date.today():
                # Parse from file if date hasn't changed
                self.sunrise = iso8601.parse_date(dates_yaml.data['sunrise'])
                self.sunset = iso8601.parse_date(dates_yaml.data['sunset'])
                self.timezone = pytz.timezone(dates_yaml.data['timezone'])
            #TODO: Can add location check here
            else:
                # Update date information
                se = SunEquation(self.latitude,self.longitude)
                se.calculate()
                output = se.format_yaml()
                self.date = output["date"]
                self.sunrise = output["sunrise"]
                self.sunset = output["sunset"]
                self.timezone = output["timezone"]
                dates_yaml.writeYaml(output)
        
    def updater(self):
        """
            This function takes the information parsed from the 
            command-line and yaml file and determines what actions to take.
        """
        self.update_sun()
        # find image when not supplied by the commandline 
        if self.wallpaper_file is None:
            wallpapers = self.load_csv()
            self.select_wallpaper(wallpapers)
        self.set_wallpaper()

    def load_csv(self):
        """
            Reads in the csv file and loads the data into memory.
        """
        read_file = CSVFileIO(self.csvfile)
        data = read_file.readFile()
        logging.debug("Number of lines read from csv file: " + str(len(data)))
        return data

    def select_wallpaper(self, data):
        """ 
            Selects the wallpaper to be set as deesktop background.
        """
        # Search criterion reduces length of class here
        chosen_image = randomiser(data)
        self.wallpaper_file = Path(str(chosen_image['path']))
        logging.debug("chosen image: "  + str(self.wallpaper_file))

    def set_wallpaper(self):
        """
            Updates the wallpaper by creating a WallpaperChanger object 
            and calling the apply_new_wallpaper method.
        """
        wallpaper_changer = WallpaperChanger(self.wallpaper_file)
        wallpaper_changer.apply_new_wallpaper()

    def set_theme(self):
        """
            Set xfce theme.
        """
        pass

class WallpaperChanger:
    """ The DesktopChanger class can be used to read and set the 
    wallpaper when provided with an image.
    """
    cmd_wallpaper_read = "xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image"
    cmd_wallpaper_set = "xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image --set "

    def __init__(self, wallpaper_file):
        """Takes the new wallpaper_file selected. Then the current 
        wallpaper is read from xfconf-query.
        * wallpaper_file should be a PosixPath object
        """
        try:
            self.wallpaper = wallpaper_file
            self.old_wallpaper = WallpaperChanger.current_wallpaper()
            if not self.wallpaper.is_file():
                raise FileNotFoundError
        except FileNotFoundError:
            print("The wallpaper file doesn't exist. \n")
            raise

    @staticmethod
    def current_wallpaper():
        """ read current wallpaper being applied from xfconf-query.
        Returns a Path object stripped of bash wrapping.
        """
        try:
            output = subprocess.check_output(
                WallpaperChanger.cmd_wallpaper_read, shell='/bin/bash')
        except subprocess.CalledProcessError as e_info:
            print("subprocess did not run successfully. " + str(e_info))
            raise
        return Path(output.strip().decode())

    def apply_new_wallpaper(self):
        """Updates the wallpaper if the current new image is different to 
        the current image. Otherwise it does nothing.
        """
        try:
            if self.old_wallpaper != self.wallpaper:
                cmd = (WallpaperChanger.cmd_wallpaper_set 
                    + repr(str(self.wallpaper)))
                cmd_output = subprocess.run(cmd, shell='/bin/bash')
                logging.debug(cmd_output)
        except subprocess.CalledProcessError:
            print("subprocess did not run successfully. ")
            raise
