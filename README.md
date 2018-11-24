# Desktop wallpaper changer

Ultimate aim of this project is to be able to adjust the wallpaper (and in future xfce panels) of the desktop depending on the the time and day. In this manner daytime wallpapers can have a blue theme and bright theme whilst during the night the theme can be red and dull.

## Prerequistes

* XFCE system

### Configuration

A config.yaml file is needed in the same directory and the latitude and longitude values for the current position must be supplied. 
!! North and West are positive values whilst East and South are negative values.

## Running the script

The following command can be run to update the desktop background:

`python3 updatedesktop.py`
`python3 wallpaperscanner.py`

## Phase 2

* Analyse each image and save certain properties

## Phase 3

* Calculate how much blue/red light the background wallpaper should have depending on the  time, date and latitude 
* Use the above criteria to narrow down images to randomly select from
