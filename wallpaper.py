#!/usr/bin/python3

import subprocess
from pathlib import Path
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("image", help="Full image file location to be set to the \
                                    desktop background.")
args =parser.parse_args()
arg_wallpaper = args.image

logging.basicConfig(filename=('desktopchanger.log'),level=logging.DEBUG)

class WallpaperChanger:
    """ The DesktopChanger class can be used to read and set the wallpaper 
    when provided with an image.
    """
    cmd_wallpaper_read = "xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image"
    cmd_wallpaper_set = "xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image --set "

    def __init__(self, wallpaper_file):
        """Checks some of the inputs to ensure the new file will not break 
        xfconf-query.
        """
        try:
            self.wallpaper = Path(wallpaper_file)
            if not self.wallpaper.is_file():
                raise FileNotFoundError
        except FileNotFoundError as e_info:
            print("The wallpaper file doesn't exist the wallpaper folder \n"
                + e_info)
            raise

    def current_wallpaper(self):
        """ read current wallpaper being applied from xfconf-query.
        """
        output = subprocess.check_output(WallpaperChanger.cmd_wallpaper_read, 
            shell='/bin/bash')
        return output

    def apply_new_wallpaper(self):
        """Updates the wallpaper if the current new image is different to the 
        current image. Otherwise it does nothing.
        """
        old_wallpaper = self.current_wallpaper() 
        if old_wallpaper != self.wallpaper:
            cmd = WallpaperChanger.cmd_wallpaper_set + str(self.wallpaper)
            cmd_output = subprocess.run(cmd, shell='/bin/bash')
            logging.debug(cmd_output)
            print(cmd_output) #TODO: remove when everything is working properly

# Main Script body
logging.debug("Executing wallpaper.py")
if not arg_wallpaper is None:
    wallpaper_changer = WallpaperChanger(arg_wallpaper)
else:
    pass
old_wallpaper = wallpaper_changer.current_wallpaper()
logging.debug(str("old wallpaper path: ", old_wallpaper)) 
wallpaper_changer.apply_new_wallpaper()
