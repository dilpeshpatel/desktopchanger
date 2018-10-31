#!/usr/bin/python3
"""This script can be used to traverse a given folder path for images 
and append these images to a stored csv file.
"""

import logging
import argparse
from desktopchanger.findwallpapers import LoadImages

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
    args = cmd_arguments()
    image_loader  = LoadImages(args)
    image_loader.loadimages()
    print("success")