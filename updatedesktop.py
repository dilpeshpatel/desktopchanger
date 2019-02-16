#!/usr/bin/python3
"""This script can be used to update desktop properties depending on
the flags specified.

Future arguments:
* update panels only
* toggle default on/off
* toggle default-scheme: night/day
"""

import logging
import argparse
from desktopchanger.desktopchanger import DesktopChanger

logging.basicConfig(filename=('logs/desktopchanger.log'), level=logging.DEBUG)

###### Argument Parsing
######
def cmd_arguments():
    """
        taking CMD arguments and sending them through the argument
        parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image",
                        help="Full image path can be optionally supplied.")
    args = parser.parse_args()
    return args

##### Main
#####
if __name__ == "__main__":
    args = cmd_arguments()
    update_desktop = DesktopChanger(args)
    update_desktop.updater()
    print("success")
