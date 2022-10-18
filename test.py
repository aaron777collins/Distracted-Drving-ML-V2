import numpy as np
import pandas as pd

import os.path as path
from gatherData import Gatherer
from EasyMLLib.helper import Helper

DIB_NAME = "DIB2"
DATASETS_PATH = path.join("data", DIB_NAME, 'dataRaw', 'ID') #possibly wrong rn
SELECTED_DATA_SET_PATH = path.join("Single", "ET")
CONCAT_FILE_PATH = path.join("data", DIB_NAME)
CONCAT_FILE_NAME = "concat-data"
CONCAT_FILE_EXT = ".csv"
CONCAT_FULLPATH_WITHOUT_EXT = path.join(CONCAT_FILE_PATH, CONCAT_FILE_NAME) #data data/DIB2/-data


class DataCleaner:
    def main(self):
            data: pd.DataFrame = self.gatherECGDataConcat(overwrite=True)
            #Helper.quickDfStat(data)

    def gatherECGDataConcat(self, overwrite=False) -> pd.DataFrame:
        CONCAT_FULL_PATH_WITH_EXT_CLEANED = CONCAT_FULLPATH_WITHOUT_EXT + \
            "-concat" + '-valid-cleaned' + CONCAT_FILE_EXT #data\DIB2\concat-data-concat-valid-cleaned.csv 
        
        CONCAT_FULL_PATH_WITH_EXT = CONCAT_FULLPATH_WITHOUT_EXT + "-concat" + CONCAT_FILE_EXT

        print(f"CONCAT_FULL_PATH_WITH_EXT_CLEANED: {CONCAT_FULL_PATH_WITH_EXT_CLEANED} \n" );

        print(f"CONCAT_FULL_PATH_WITH_EXT: {CONCAT_FULL_PATH_WITH_EXT} \n" );

        # if not path.exists(CONCAT_FULL_PATH_WITH_EXT_CLEANED) or overwrite:
        #     print(f"{CONCAT_FULL_PATH_WITH_EXT_CLEANED} not found! Cleaning data..")
        #     data = self.ensureConcatECGDataGathered()
        #     return self.cleanData(data, CONCAT_FULL_PATH_WITH_EXT_CLEANED)
        # else:
        #     print(f"{CONCAT_FULL_PATH_WITH_EXT_CLEANED} found! Reading data..")
        #     return pd.DataFrame(pd.read_csv(CONCAT_FULL_PATH_WITH_EXT_CLEANED))

if __name__ == "__main__":
    DataCleaner().main()