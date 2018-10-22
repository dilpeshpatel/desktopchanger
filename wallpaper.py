#!/usr/bin/env python3

from pathlib import Path
import subprocess

# global variables to use
wallpaper_folder = ''
a = ''
b = ''
c = ''

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
            new_wallpaper = Path(Path.home(), wallpaper_folder)
            if not new_wallpaper.is_dir():
                raise NotADirectoryError
            self.wallpaper = new_wallpaper / wallpaper_file
            """ The following few lines of code doesn't seem to work for this
            version of python. (maybe fixed in a later version of 3.5.4-5)
            """
            # if not new_wallpaper.is_file():
            #     raise FileNotFoundError
        except NotADirectoryError as e_info:
            print("Wallpaper folder must be a directory")
            raise
        except FileNotFoundError as e_info:
            print("The wallpaper file doesn't exist the wallpaper folder")
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
            print(cmd_output)


wallpaper_changer = WallpaperChanger(c)
old_wallpaper = wallpaper_changer.current_wallpaper()
print(old_wallpaper)
wallpaper_changer.apply_new_wallpaper()
