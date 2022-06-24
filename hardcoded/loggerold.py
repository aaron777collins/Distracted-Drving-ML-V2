from datetime import datetime
import os.path as path
import string
from typing import Tuple

import numpy as np
import pandas as pd

DIB_NAME = "DIB1"
DATASETS_PATH = path.join(DIB_NAME, 'dataRaw', 'ID')
SELECTED_DATA_SET_PATH = path.join("Single", "ET")
CONCAT_FILE_PATH = DIB_NAME
CONCAT_FILE_NAME = "concat-data"
CONCAT_FILE_EXT = ".csv"
CONCAT_FULLPATH_WITHOUT_EXT = path.join(CONCAT_FILE_PATH, CONCAT_FILE_NAME)
OUTPUT_FOLDER_PATH = path.join("Outputs", "Output")

class LoggerOld:
    def __init__(self, name: string):
        self.name = name
        timeLog = datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S')
        self.log("### "+ timeLog + " ###")
        
        
    def log(self, *args):
        with open(path.join(OUTPUT_FOLDER_PATH, self.name), "a+") as file:
            for elem in args:
                print(str(elem) + " ", end='')
                file.write(str(elem) + " ")
            file.write("\n")
            print()