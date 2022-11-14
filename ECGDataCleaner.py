import numpy as np
import pandas as pd

import os.path as path
from ECGgatherData import ECGGatherer
from EasyMLLib.helper import Helper

DIB_NAME = "DIB2"
DATASETS_PATH = path.join("data", DIB_NAME, 'dataRaw') #possibly wrong rn
SELECTED_DATA_SET_PATH = path.join("Single", "ET")
CONCAT_FILE_PATH = path.join("data", DIB_NAME)
CONCAT_FILE_NAME = "concat-data"
CONCAT_FILE_EXT = ".csv"
CONCAT_FULLPATH_WITHOUT_EXT = path.join(CONCAT_FILE_PATH, CONCAT_FILE_NAME) #data data/DIB2/concat-data

class ECGDataCleaner:

    def main(self):
        data: pd.DataFrame = self.gatherECGDataConcat(overwrite=True)
        Helper.quickDfStat(data)

    def gatherECGDataConcat(self, overwrite=False) -> pd.DataFrame:
        CONCAT_FULL_PATH_WITH_EXT_CLEANED = CONCAT_FULLPATH_WITHOUT_EXT + \
            "-concat" + '-valid-cleaned' + CONCAT_FILE_EXT #data\DIB2\concat-data-concat-valid-cleaned.csv 

        #if data not found we need to clean and post it to files
        if not path.exists(CONCAT_FULL_PATH_WITH_EXT_CLEANED) or overwrite:
            print(f"{CONCAT_FULL_PATH_WITH_EXT_CLEANED} not found! Cleaning data..")
            data = self.ensureConcatECGDataGathered()
            return self.cleanData(data, CONCAT_FULL_PATH_WITH_EXT_CLEANED)
        # read the cleaned data
        else:
            print(f"{CONCAT_FULL_PATH_WITH_EXT_CLEANED} found! Reading data..")
            return pd.DataFrame(pd.read_csv(CONCAT_FULL_PATH_WITH_EXT_CLEANED))

    def ensureConcatECGDataGathered(self) -> pd.DataFrame:

        CONCAT_FULL_PATH_WITH_EXT = CONCAT_FULLPATH_WITHOUT_EXT + "-concat" + CONCAT_FILE_EXT #data\DIB2\concat-data-concat.csv
        
        #if data not found we need to gather and post it to files
        if not path.exists(CONCAT_FULL_PATH_WITH_EXT):
            print(f"{CONCAT_FULL_PATH_WITH_EXT} not found! Gathering data..")
            gatherer = ECGGatherer()
            return gatherer.gatherDataConcat() #this is a dataFrame

        # read the cleaned data
        else:
            print(f"{CONCAT_FULL_PATH_WITH_EXT} found! Reading data..")
            return pd.DataFrame(pd.read_csv(CONCAT_FULL_PATH_WITH_EXT))

    def cleanData(self, data: pd.DataFrame, pathStr: str) -> pd.DataFrame:
        print(f"Saving {pathStr}")
        data.to_csv(pathStr, index=False)
        return data


if __name__ == "__main__":
    ECGDataCleaner().main()
