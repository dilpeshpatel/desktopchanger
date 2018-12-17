""" The classes contained here are designed to traverse a given folder 
and find images files.
This will be turned into a database set at a later date.
For now the behaviour is to analyse each image in a single directory 
and extract the full path and some information about the image.

Improvements
*fieldnames variable should only exist in one place
"""

import logging
from pathlib import Path
from collections import deque
from desktopchanger.utils import yamlFileIO, CSVFileIO
from desktopchanger.imageanalysis import ImageAnalysis

# common image types
image_formats={".jpg",".jpeg", ".png"}

##### Classes
#####
class WallpaperSearch:
    """This class is used to take a folder path and retreive all image
    files held within.
    """
    def __init__(self, args):
        try:
            self.imagelist = []
            yaml_config = yamlFileIO("", "config.yaml")
            yaml_config.readYaml()
            # Setting base wallpaper folder
            if args.folder is not None:
                self.folder = Path(str(args.folder))
            else:
                self.folder = Path(str(yaml_config.data['wallpapersFolder']))
            if not self.folder.is_dir():
                raise NotADirectoryError
            #setting up csv_io
            csv_file = yaml_config.data['csvFile']
            self.csv_io = CSVFileIO(csv_file)
        except NotADirectoryError:
            print("The path supplied must be a folder \n")
            raise

    def searchFolder(self):
        """Main method to call from object to process nested paths to 
        build a list of images which are then saved to file.
        """
        image_files = self.processPath()
        self.processImages(image_files)
        self.saveCSV()

    def processPath(self):
        """ Convert the folder and path into a list of additional
        folders to search through and files to check if they are
        images.
        All image files are returned as a list.
        """
        image_files = []
        folderlist = [self.folder]
        while folderlist:
            filelist, newfolderslist = WallpaperSearch.processFolder(
                Path(folderlist.pop()))
            folderlist.extend(newfolderslist)
            image_files.extend(filelist)
        return image_files

    @staticmethod
    def processFolder(folder):
        """The specified folder will be traversed and a list of images 
        are built into one list with folders in another.
        """
        filelist =  []
        folderlist = []
        for child in folder.iterdir():
            if child.suffix.lower() in image_formats and child.is_file():
                relative_path = child.relative_to(Path.home())
                filelist.append(relative_path)
            elif child.is_dir():
                folderlist.append(child)
                logging.debug("Found new folder: {}".format(child.name))
        logging.debug("Found images: " + str(len(filelist)))
        return filelist, folderlist

    def processImages(self, image_files):
        """Process the list of image paths, analyse each image and turn
        the list into a dict. TODO: analyse each image
        """
        self.imagelist.clear()
        for path in image_files:
            #Analyse each image for hues and brightness balance
            path_str = str(Path(Path.home(),path))
            image_analyse = ImageAnalysis(path_str)
            blue, green, red, light, dark = image_analyse.analyse_hsv()
            dictonary = self.dict_formatter(path_str, blue, green, red, light, dark)
            self.imagelist.append(dictonary)

    def saveCSV(self):  
        """Save the list of images to disk.
        """
        # csvWriter = CSVFileIO(self.csv_file)
        fieldnames = ['path', 'blue', 'green', 'red', 'light', 'dark']
        self.csv_io.writeFile(self.imagelist, fieldnames)
        
    def dict_formatter(self, path, blue, green, red, light, dark):
        """
            Dictionary object to be constructed to save data to file.
            Note: This way seems terribly inefficient.
        """
        fieldnames = ['path', 'blue', 'green', 'red', 'light', 'dark']
        data = [ path, round(blue, 5), round(green, 5), round(red, 5), 
            round(light, 5), round(dark, 5) ]
        output = dict(zip(fieldnames, data))
        return output



