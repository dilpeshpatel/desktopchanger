# Desktop wallpaper changer

Ultimate aim of this project is to be able to adjust the wallpaper (and in future xfce panels) of the desktop depending on the the time and day. In this manner daytime wallpapers can have a blue theme and bright theme whilst during the night the theme can be red and dull.

## Prerequistes

* XFCE system
* separate virtual environment created for this project.
* Cron installed

## Configuration

### Setup
1. Create a directory called `data` and place an empty file called `dates.yaml` within.
1. Create a directory called `logs`.

### Yaml 
1. Open the `config.yaml` file.
1. Set the wallpapersFolder variable to the directory containing the wallpaper images.
1. Set the longitude and latitude variables to the current city. 
!! North and West are positive values whilst East and South are negative values.

### Cron 
Cron is used to automate running the update wallpaper script at a set time interval. 

> Because cron is run as the root user the user environment variables containing the display session are not available. To get around this issue this project has introduced a bash script which sets the necessary environmental variables.

#### Bash script
Before it can be used the bash script must also be configured. 

1. Open the '/scripts/desktopchanger.sh' file
1. Complete the path on the fifth line starting "source" which points from the home directory to the virtual environment activation script. 
1. Set the 'PROJECT_FOLDER' path to point from the home directory to the project folder directory. (Include a trailing '/')
1. Test running the script works from a new terminal.

#### Cron Task
Append the line to crontab (e.g. using `crontab -e`):
```
* * * * * "/<path to project from root directory>/scripts/desktopchanger.sh"  >> /<path to project from root directory>/logs/cron.log
```

The beginning sequence can be adjusted to change how often the script is run and therefore how often the wallpaper is changed. The default here is once a minute (the minimum time interval allowed)

With both the cron task and bash script setup correctly the desktop wallpaper should be updated. Ensure the `wallpaperscanner.py` script has been run successfully first.

## Running the script

Alternatively it is possible to execute the script directly from terminal. The `wallpaperscanner.py` script must be run first to analyse a list of images before the `updatedesktop.py` script can be run.  
The following command can be used to update the wallpaper or scan a directory for wallpaper images:

`python3 wallpaperscanner.py`
`python3 updatedesktop.py`