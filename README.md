# Desktop wallpaper changer

Ultimate aim of this project is to be able to adjust the wallpaper (and in future xfce panels) of the desktop depending on the the time and day. In this manner daytime wallpapers can have a blue theme and bright theme whilst during the night the theme can be red and dull.

## Prerequistes

* XFCE system

### Configuration

A config.yaml file is needed in the same directory and the latitude and longitude values for the current position must be supplied. 
!! North and West are positive values whilst East and South are negative values.

## Cron
Cron is used to automate running the update wallpaper script at a set time interval. 

> Because cron is run as the root user the user environment variables containing the display session are not available. To get around this issue this project has introduced a bash script which sets the necessary environmental variables.

### Prerequisites
* virtual environment for this project
* cron

###Bash script
The bash script `/scripts/desktopchanger.sh` needs to have paths set specifically the `PROJECT_FOLDER` environmental variable and the `source` virtual environment lines. The former line points to the project folder path and the latter is the path to virtual environment created for this project.

###Cron Task
Append the line to crontab (e.g. using `crontab -e`):
```
* * * * * "./<path to project from user home directory>/desktopchanger.sh" 
```

The beginning sequence can be adjusted to change how often the script is run and therefore how often the wallpaper is changed. The default here is once a minute (the minimum time interval allowed)

With both the cron task and bash script setup correctly the desktop wallpaper should be updated. Ensure the `wallpaperscanner.py` script has been run successfully first.

## Running the script

Alternatively it is possible to execute the script directly from terminal. The `wallpaperscanner.py` script must be run first to analyse a list of images before the `updatedesktop.py` script can be run.  
The following command can be used to update the wallpaper or scan a directory for wallpaper images:

`python3 wallpaperscanner.py`
`python3 updatedesktop.py`