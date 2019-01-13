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
def randomiser(count):
    """ Returns a random number from 0 to count.
    """
    return random.randint(0,count-1)


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
        
    def updater(self):
        """
            High level function used to:
            * get or compute sunset and sunrise times
            * set a randomised wallpaper depending on time of day
        """
        self.update_sun()
        # find image when not supplied by the commandline 
        if self.wallpaper_file is None:
            wallpapers = self.load_csv()
            self.select_wallpaper(wallpapers)
        self.set_wallpaper()

    def update_sun(self):
        """Retrieve sun information from file or update the information if the 
        day (TODO: future location) information has changed.

        sets parameter is_night_time to True or False depending on the time of 
        day.
        """
        dates_yaml = yamlFileIO("data", "dates.yaml")
        dates_yaml.readYaml()
        # Read file for date information
        if len(dates_yaml.data) is not 0:
            date = iso8601.parse_date(dates_yaml.data['date'])
            if date == datetime.date.today():
                # Parse from file if date hasn't changed
                sunrise = iso8601.parse_date(dates_yaml.data['sunrise'])
                sunset = iso8601.parse_date(dates_yaml.data['sunset'])
                timezone = pytz.timezone(dates_yaml.data['timezone'])
            #TODO: Can add location check here
            else:
                # Update date information
                se = SunEquation(self.latitude,self.longitude)
                se.calculate()
                date = datetime.date.today()
                sunrise = se.rise
                sunset = se.set
                timezone = se.timezone
                output = se.format_yaml()
                dates_yaml.writeYaml(output)
        current_time = datetime.datetime.now(timezone)
        if  current_time > sunrise and current_time < sunset:
            self.is_night_time = False
        else:
            self.is_night_time = True


    def load_csv(self):
        """
            Reads in the csv file and loads the data into memory.
        """
        read_file = CSVFileIO(self.csvfile)
        data = read_file.readFile()
        logging.debug("Number of lines read from csv file: " + str(len(data)))
        return data

    def select_wallpaper(self, all_images):
        """ 
            Selects the wallpaper to be set as desktop background.
        """
        # Search criterion reduces image list

        filtered_paths = self.slice_wallpapers(all_images, self.is_night_time)
        chosen_image = randomiser(len(filtered_paths))
        self.wallpaper_file = Path(str(filtered_paths[chosen_image]))
        logging.debug("chosen image: "  + str(self.wallpaper_file))

    def set_wallpaper(self):
        """
            Updates the wallpaper by creating a WallpaperChanger object 
            and calling the apply_new_wallpaper method.
        """
        wallpaper_changer = WallpaperChanger(self.wallpaper_file)
        wallpaper_changer.apply_new_wallpaper()

    def slice_wallpapers(self, images, is_night_time):
        """
            Remove images not fitting the day/night criteria.
            Currently the subset is day_pic + night_pic = images
        """ 
        images = images.sort_values(['red', 'blue', 'light'])
        try:
            night_images = images.loc[(images.red < 0.15) & (images.blue < 0.1) & (images.light > 0.15)]
            night_images_index = night_images.index.tolist()
            assert night_images.empty is not True
        except AssertionError as error:
            print("No images left are processing criteria")
            raise error
        day_images_index = images.loc[~images.index.isin(night_images_index)].index.tolist()
        if is_night_time:
            logging.debug("Night images sliced: {}".format(len(night_images_index)))
            return night_images_index
        else:
            logging.debug("Day images sliced: {}".format(len(day_images_index)))
            return day_images_index

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
            logging.debug("Old wallpaper is: {}".format(str(self.old_wallpaper)))
            logging.debug("New wallpaper is: {}".format(str(self.wallpaper)))
            if self.old_wallpaper != self.wallpaper:
                cmd = (WallpaperChanger.cmd_wallpaper_set 
                    + repr(str(self.wallpaper)))
                cmd_output = subprocess.run(cmd, shell='/bin/bash')
                logging.debug(cmd_output)
        except subprocess.CalledProcessError:
            print("subprocess did not run successfully. ")
            raise
