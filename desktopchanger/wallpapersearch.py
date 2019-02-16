"""
    The classes contained here are designed to traverse a given folder
    and find images files.
    This will be turned into a database set at a later date.
    For now the behaviour is to analyse each image in a single directory
    and extract the full path and some information about the image.

    Improvements
    *fieldnames variable should only exist in one place
"""

import logging
from pathlib import Path
import pandas
from desktopchanger.utils import YamlFileIO, CSVFileIO
from desktopchanger.imageanalysis import ImageAnalysis

# common image types
IMAGE_FORMATS = {".jpg", ".jpeg", ".png"}

##### Classes
#####
class WallpaperSearch:
    """
        This class is used to take a folder path and retreive all image
        files held within.
    """
    def __init__(self, args):
        try:
            self.image_data = []
            yaml_config = YamlFileIO("", "config.yaml")
            yaml_config.read_yaml()
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

    def search_folder(self):
        """
            Main method to call from object to process nested paths to
            build a list of images which are then saved to file.
        """
        image_files = self.process_path()
        self.process_images(image_files)
        self.save_file()

    def process_path(self):
        """
            Convert the folder and path into a list of additional
            folders to search through and files to check if they are
            images.
            All image files are returned as a list.
        """
        image_files = []
        folderlist = [self.folder]
        while folderlist:
            filelist, newfolderslist = WallpaperSearch.process_folder(
                Path(folderlist.pop()))
            folderlist.extend(newfolderslist)
            image_files.extend(filelist)
        return image_files

    @staticmethod
    def process_folder(folder):
        """
            The specified folder will be traversed and a list of images
            are built into one list with folders in another.
        """
        filelist = []
        folderlist = []
        for child in folder.iterdir():
            if child.suffix.lower() in IMAGE_FORMATS and child.is_file():
                relative_path = child.relative_to(Path.home())
                filelist.append(relative_path)
            elif child.is_dir():
                folderlist.append(child)
                logging.debug("Found new folder: %s", child.name)
        logging.debug("Found images: %s", str(len(filelist)))
        return filelist, folderlist

    def process_images(self, image_files):
        """
            Process the list of image paths, analyse each image and turn
            the list into a dict. TODO: analyse each image
        """
        imagelist = []
        for path in image_files:
            #Analyse each image for hues and brightness balance
            path_str = str(Path(Path.home(), path))
            image_analyse = ImageAnalysis(path_str)
            blue, green, red, light, dark = image_analyse.analyse_hsv()
            dictonary = self.dict_formatter(path_str, blue, green, red, light, dark)
            imagelist.append(dictonary)
        data_frame = pandas.DataFrame(imagelist)
        self.image_data = data_frame.sort_values(['red', 'blue', 'light'])

    def save_file(self):
        """
            Save the list of images to disk.
        """
        fieldnames = ['path', 'blue', 'green', 'red', 'light', 'dark']
        self.csv_io.write_file(self.image_data, fieldnames)

    def dict_formatter(self, path, blue, green, red, light, dark):
        """
            Dictionary object to be constructed to save data to file.
            Note: This way seems terribly inefficient.
        """
        fieldnames = ['path', 'blue', 'green', 'red', 'light', 'dark']
        data = [path, round(blue, 3), round(green, 3), round(red, 3),
                round(light, 3), round(dark, 3)]
        output = dict(zip(fieldnames, data))
        return output
