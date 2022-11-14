import os.path as path
import string
from EasyMLLib.helper import Helper
from EasyMLLib.DataGatherer import DataGatherer

import pandas as pd

DIB_NAME = "DIB2"
DATASETS_PATH = path.join("data", DIB_NAME, 'dataRaw') #possibly wrong rn
SELECTED_DATA_SET_PATH = path.join("ECG")
CONCAT_FILE_PATH = path.join("data", DIB_NAME)
CONCAT_FILE_NAME = "concat-data"
CONCAT_FILE_EXT = ".csv"
CONCAT_FULLPATH_WITHOUT_EXT = path.join(CONCAT_FILE_PATH, CONCAT_FILE_NAME) #data data/DIB2/concat-data

CLASSIFIERS = [0, 2]

MIN_ID = 1
MAX_ID = 16

class ECGGatherer:
    def main(self):
        self.gatherDataConcat()

    def getProperIdNumber(self, idNum) -> string: 
        if (idNum >= 10):
            return f'{idNum}'
        else:
            return f'0{idNum}'


    # Gathers the data for a given id
    def gatherData(self, idNum) -> pd.DataFrame:
        CONCAT_FULL_PATH_WITH_EXT = CONCAT_FULLPATH_WITHOUT_EXT + \
            "-" + str(idNum) + CONCAT_FILE_EXT #data/DIB2/concat-data-2.csv

        # Function called when the file isn't found
        def concatFunc() -> pd.DataFrame:
            id = f"0{idNum}"
            dfs = []
            for classifier in CLASSIFIERS:

                # hardcoded case to skip 11 because they dont have 0 back
                if (idNum == 11 and classifier == 0):
                    continue

                idNumberCleaned = self.getProperIdNumber(idNum)

                filePath = path.join(
                    DATASETS_PATH , f'ID{idNumberCleaned}', SELECTED_DATA_SET_PATH, f'ID{idNumberCleaned}_ECG_{classifier}Back.csv') #ID01/ECG/ID01_ECG_0Back.csv
                print(filePath)
                tmpDf: pd.DataFrame = pd.DataFrame(pd.read_csv(filePath, usecols =[0,1], names=['time', 'SP']))
                
                tmpDf['classifier'] = classifier
                #Helper.quickDfStat(tmpDf)
                dfs.append(tmpDf)
            
            finalDf = pd.concat(dfs)
            print("Concatenated!")
            #Helper.quickDfStat(finalDf)
            finalDf.to_csv(CONCAT_FULL_PATH_WITH_EXT, index=False)
            print(f"Saved: {CONCAT_FULL_PATH_WITH_EXT}")
            return finalDf

        df = DataGatherer().gatherDataFromFile(
            CONCAT_FULL_PATH_WITH_EXT, concatFunc=concatFunc)
        # Helper.quickDfStat(df)
        return df

    def gatherDataConcat(self) -> pd.DataFrame:
        CONCAT_FINAL_FULL_PATH_WITH_EXT = CONCAT_FULLPATH_WITHOUT_EXT + \
            "-concat" + CONCAT_FILE_EXT #data/DIB2/concat-data-concat.csv

        # Function called when the file isn't found
        def concatFunc() -> pd.DataFrame:
            dfArr: list[pd.DataFrame] = []

            for idNum in range(MIN_ID, MAX_ID+1):
                dfArr.append(self.gatherData(idNum))

            finalDf = pd.concat(dfArr)
            print("Concatenated!")
            Helper.quickDfStat(finalDf)
            finalDf.to_csv(CONCAT_FINAL_FULL_PATH_WITH_EXT, index=False)
            print(f"Saved: {CONCAT_FINAL_FULL_PATH_WITH_EXT}")
            return finalDf

        df = DataGatherer().gatherDataFromFile(
            CONCAT_FINAL_FULL_PATH_WITH_EXT, concatFunc=concatFunc)
        Helper.quickDfStat(df)
        return df


if __name__ == "__main__":
    ECGGatherer().main()
