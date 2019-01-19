#!/bin/bash

echo "Begin wallpaper.sh script"
PROJECT_FOLDER=<path to folder>
source ~/<path to virtual env folder>/bin/activate
set -x
PID=$(echo $(ps -C xfce4-session -o pid=))                                      
export $(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ)
export DISPLAY=:0.0
cd ${HOME}${PROJECT_FOLDER}
python updatedesktop.py >> ${HOME}${PROJECT_FOLDER}/logs/bash.log
echo "updatedesktop.py Script complete"
