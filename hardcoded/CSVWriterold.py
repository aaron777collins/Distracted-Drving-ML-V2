from csv import writer
from datetime import datetime
import os.path as path
import string
from typing import List, Tuple

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

class CSVWriterOld:
    def __init__(self, name: string, columns: List[str]):
        self.name = name
        self.columns = columns
        with open(path.join(OUTPUT_FOLDER_PATH, self.name), "a+", newline='') as file:
                writerObj = writer(file)
                writerObj.writerow(columns)
        
        
    def addRow(self, row: list):
        with open(path.join(OUTPUT_FOLDER_PATH, self.name), "a+", newline='') as file:
            writerObj = writer(file)
            writerObj.writerow(row)