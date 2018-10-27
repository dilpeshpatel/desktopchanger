#!/usr/bin/python3

import subprocess
from pathlib import Path
import logging
import os
import argparse

import yaml

logging.basicConfig(filename=('desktopchanger.log'),level=logging.DEBUG)

class WallpaperChanger:
    """ The DesktopChanger class can be used to read and set the wallpaper 
    when provided with an image.
    """
    cmd_wallpaper_read = "xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image"
    cmd_wallpaper_set = "xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image --set "

    def __init__(self, wallpaper_file):
        """Takes the new wallpaper_file selected. Then the current wallpaper
        is read from xfconf-query
        """
        try:
            self.wallpaper = Path(wallpaper_file)
            self.old_wallpaper = WallpaperChanger.current_wallpaper()
            if not self.wallpaper.is_file():
                raise FileNotFoundError
        except FileNotFoundError as e_info:
            print("The wallpaper file doesn't exist the wallpaper folder \n"
                + e_info)
            raise

    def current_wallpaper():
        """ read current wallpaper being applied from xfconf-query.
        Returns a Path object.  
        """
        try:
            output = subprocess.check_output(WallpaperChanger.cmd_wallpaper_read, 
                shell='/bin/bash')
        except subprocess.CalledProcessError as e_info:
            print("subprocess did not run successfully. " + str(e_info))
            raise

        return Path(output.strip().decode())

    def apply_new_wallpaper(self):
        """Updates the wallpaper if the current new image is different to the 
        current image. Otherwise it does nothing.
        """
        try:
            if self.old_wallpaper != self.wallpaper:
                cmd = WallpaperChanger.cmd_wallpaper_set + str(self.wallpaper)
                cmd_output = subprocess.run(cmd, shell='/bin/bash')
                logging.debug(cmd_output)
        except subprocess.CalledProcessError as e_info:
            print("subprocess did not run successfully. " + str(e_info))
            raise


###### Argument Parsing
######

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", 
    help="Full image path can be optionally supplied.")
args =parser.parse_args()
arg_wallpaper = args.image



###### Main Script body
######

logging.debug("Executing wallpaper.py")
if arg_wallpaper is None:
    """This is the default operation where an image is randomly selected and
    applied as the new wallpaper.
    """
    logging.debug("Nothing currently happens without specifying a wallpaper")
    print("Nothing currently happens without specifying a wallpaper")
else:
    """When an image path is provided optionally it is applied as the wallpaper.
    """
    wallpaper_changer = WallpaperChanger(arg_wallpaper)
    wallpaper_changer.apply_new_wallpaper()