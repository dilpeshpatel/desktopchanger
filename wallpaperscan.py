#!/usr/bin/python3
"""
    This script can be used to traverse a given folder path for
    images and append these images to a stored csv file.
    These images are analysed for light, darkness balance and red,
    blue and green channels as percentage of pixels in image.
"""

import logging
import argparse
import time
from desktopchanger.wallpapersearch import WallpaperSearch

logging.basicConfig(filename=('logs/wallpapercsv.log'), level=logging.DEBUG)

##### Argument Parsing
#####
def cmd_arguments():
    """
        taking CMD arguments and sending them through the argument
        parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder",
                        help="Full wallpapers folder path can be optionally supplied.")
    args = parser.parse_args()
    return args

##### Main
#####
if __name__ == "__main__":
    start_time = time.time()
    ARGS = cmd_arguments()
    image_loader = WallpaperSearch(ARGS)
    image_loader.search_folder()
    end_time = time.time()
    logging.debug("--- %s seconds --- {}", (end_time - start_time))
    print("--- %s seconds ---" % (end_time - start_time))
    print("success")
