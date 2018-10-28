#!/bin/bash

conf_home=<path_HOME>
project_folder=<path_to_project_from_home>
set -x
PYTHONHOME=/usr/lib/python3.5
export DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-8G2jKeGwda
DISPLAY=:0.0
cd <path_to_project_folder>
/usr/bin/python3.5 wallpaper.py >> <path_to_random_folder>/something.log
echo "DesktopChanger Script complete"
