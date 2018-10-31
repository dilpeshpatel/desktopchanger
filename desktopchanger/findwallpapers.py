""" The classes contained here are designed to traverse a given folder 
and find images files.
This will be turned into a database set at a later date.
For now the behaviour is to analyse each image in a single directory 
and extract the full path and some information about the image.
"""

import logging
from pathlib import Path
from collections import deque
from desktopchanger.utils import parse_yaml, CSVFileIO

# common image types
image_formats={".jpg",".jpeg", ".png"}

##### Classes
#####
class LoadImages:
    """This class is used to take a folder path and retreive all image
    files held within.
    """
    def __init__(self, args):
        try:
            self.imagelist = []
            yaml_config = parse_yaml()
            if args.folder is not None:
                self.folder = Path(str(args.folder))
            else:
                self.folder = Path(str(yaml_config['wallpapersFolder']))
            if not self.folder.is_dir():
                raise NotADirectoryError
            self.csv_file = yaml_config['csvFile']
        except NotADirectoryError:
            print("The path supplied must be a folder \n")
            raise

    def loadimages(self):
        """Main method to call from object to process nested paths to 
        build a list of images which are then saved to file.
        """
        images = self.processPath()
        self.processImages(images)
        self.saveCSV()

    def processPath(self):
        """Take the folder path specified and find all images nested 
        within this folder.
        """
        images = []
        folderlist = [self.folder]
        while folderlist:
            filelist, newfolderslist = LoadImages.processFolder(
                Path(folderlist.pop()))
            folderlist.extend(newfolderslist)
            images.extend(filelist)
        return images

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
                logging.debug("Found new folder: " + child.name)
        logging.debug("Found images: " + str(len(filelist)))
        return filelist,folderlist

    def processImages(self, images):
        """Process the list of image paths, analyse each image and turn
        the list into a dict. TODO: analyse each image
        """
        self.imagelist.clear()
        for path in images:
            #add image analysis here
            self.imagelist.append({"path":Path(Path.home(),path)})

    def saveCSV(self):
        """Save the list of images to disk.
        """
        csvWriter = CSVFileIO(self.csv_file)
        csvWriter.writeFile(self.imagelist)
        