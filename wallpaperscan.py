#!/usr/bin/python3
"""This script can be used to traverse a given folder path for images 
and append these images to a stored csv file.
Analysing the images in order to 
"""

import logging
import argparse
import time
from desktopchanger.wallpapersearch import WallpaperSearch

logging.basicConfig(filename=('logs/wallpapercsv.log'),level=logging.DEBUG)

##### Argument Parsing
#####
def cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder",
                        help="Full wallpapers folder path can be optionally supplied.")
    args =parser.parse_args()
    return args

##### Main
#####
if __name__ == "__main__":
    start_time = time.time()
    args = cmd_arguments()
    image_loader  = WallpaperSearch(args)
    image_loader.searchFolder()
    end_time = time.time()
    logging.debug("--- %s seconds --- {}".format(end_time - start_time))
    print("--- %s seconds ---" % (end_time - start_time))
    print("success")