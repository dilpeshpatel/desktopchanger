""" This file contains shared classes and functions.
    * imageStruct is just there for reference purposes and to allow the 
    fieldname variable to be set when saving to csv.
    * parse_yaml returns the contents of the config.yaml file as a dict
    * CSVFileIO is used to read from or write to a .csv file.
    config.yaml.
"""
import logging
import os
from pathlib import Path
import csv
import pandas
import yaml

##### Classes
#####
class CSVFileIO:
    """ This class is used to read and write to data to and from a 
    chosen csv file.
    """
    def __init__(self, csvfile):
        self.data = []
        folder = os.path.join(os.getcwd(),"data")
        self.path = os.path.join(folder, csvfile)

    def readFile(self):
        """ Reads the entire csv file.
        """
        self.data.clear()
        self.data = pandas.read_csv(self.path, index_col='path')
        logging.debug("Rows: read: {}".format(len(self.data)))
        return self.data

    def writeFile(self, data, fieldnames):
        """ Writes wallpapers to a csv file.
        """
        data.to_csv(self.path,index=False, columns=fieldnames)

class yamlFileIO:
    """Allows the reading and writing of yaml files including opening a
    parsed object.
    """
    def __init__(self, folder, yamlfile):
        self.data = {}
        self.path = Path(folder, yamlfile)
        
    def readYaml(self):
        """Reads from yaml file only if the yaml file exists. Otherwise
        it returns without doing anything.
        """
        if not self.path.is_file():
            return
        try: 
            with self.path.open('r') as f:
                self.data = yaml.load(f) 
        except IOError as e_info: 
            print(e_info) 
            raise
        except yaml.YAMLError as e_info: 
            print("Failed to import file") 
            raise 

    def writeYaml(self, output):
        """
            Write dictionary object to yaml file.
        """
        try:
            with self.path.open('w') as f:
                yaml.dump(output, f, default_flow_style=False)
        except IOError as e_info:
            print(e_info)
            raise
