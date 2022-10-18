import os.path as path
from EasyMLLib.helper import Helper
from EasyMLLib.DataGatherer import DataGatherer

import pandas as pd

DIB_NAME = "DIB1"
DATASETS_PATH = path.join("data", DIB_NAME, 'dataRaw', 'ID')
SELECTED_DATA_SET_PATH = path.join("Single", "ET")
CONCAT_FILE_PATH = path.join("data", DIB_NAME)
CONCAT_FILE_NAME = "concat-data"
CONCAT_FILE_EXT = ".csv"
CONCAT_FULLPATH_WITHOUT_EXT = path.join(CONCAT_FILE_PATH, CONCAT_FILE_NAME)

CLASSIFIERS = [0, 1, 2]

MIN_ID = 1
MAX_ID = 28

class ECGGatherer:
    def main(self):
        self.gatherDataConcat()

    # # Gathers the data for a given id
    # def gatherData(self, idNum) -> pd.DataFrame:
    #     CONCAT_FULL_PATH_WITH_EXT = CONCAT_FULLPATH_WITHOUT_EXT + \
    #         "-" + str(idNum) + CONCAT_FILE_EXT

    #     # Function called when the file isn't found
    #     def concatFunc() -> pd.DataFrame:
    #         id = f"0{idNum}"
    #         dfs = []
    #         for classifier in CLASSIFIERS:
    #             filePath = path.join(
    #                 DATASETS_PATH + f'{idNum}'.zfill(2), SELECTED_DATA_SET_PATH, f'ID{id}_ET_{classifier}.xlsx')
    #             print(filePath)
    #             tmpDf: pd.DataFrame = pd.DataFrame(pd.read_excel(filePath), columns=['FPOGX', 'FPOGY', 'FPOGS', 'FPOGD', 'FPOGID', 'FPOGV', 'BPOGX', 'BPOGY',
    #                                                'BPOGV', 'CX', 'CY', 'CS', 'LPCX', 'LPCY', 'LPD', 'LPS', 'LPV', 'RPCX', 'RPCY', 'RPD', 'RPS', 'RPV', 'BKID', 'BKDUR', 'BKPMIN'])
    #             tmpDf['classifier'] = classifier
    #             Helper.quickDfStat(tmpDf)
    #             dfs.append(tmpDf)
    #         finalDf = pd.concat(dfs)
    #         print("Concatenated!")
    #         Helper.quickDfStat(finalDf)
    #         finalDf.to_csv(CONCAT_FULL_PATH_WITH_EXT, index=False)
    #         print(f"Saved: {CONCAT_FULL_PATH_WITH_EXT}")
    #         return finalDf

    #     df = DataGatherer().gatherDataFromFile(
    #         CONCAT_FULL_PATH_WITH_EXT, concatFunc=concatFunc)
    #     # Helper.quickDfStat(df)
    #     return df

    def gatherDataConcat(self) -> pd.DataFrame:
        CONCAT_FINAL_FULL_PATH_WITH_EXT = CONCAT_FULLPATH_WITHOUT_EXT + \
            "-concat" + CONCAT_FILE_EXT

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
