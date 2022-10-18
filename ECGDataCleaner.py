import numpy as np
import pandas as pd

import os.path as path
from ECGgatherData import ECGGatherer
from EasyMLLib.helper import Helper

DIB_NAME = "DIB2"
DATASETS_PATH = path.join("data", DIB_NAME, 'dataRaw', 'ID') #possibly wrong rn
SELECTED_DATA_SET_PATH = path.join("Single", "ET")
CONCAT_FILE_PATH = path.join("data", DIB_NAME)
CONCAT_FILE_NAME = "concat-data"
CONCAT_FILE_EXT = ".csv"
CONCAT_FULLPATH_WITHOUT_EXT = path.join(CONCAT_FILE_PATH, CONCAT_FILE_NAME) #data data/DIB2/-data

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
        # Dropping these rows:
        # fpogs (start time since init of pog)
        # fpogid (id of the gaze.. which is duplicate info since fpogd shows duration)
        # CS (cursor position id)
        # CX and CY (Cursor POS)

        # data.drop(['FPOGS', 'FPOGID', 'CS', 'CX', 'CY'], axis=1, inplace=True)
        data.drop(['FPOGS', 'FPOGID', 'CS', 'CX', 'CY', 'BKID',
                  'BKDUR', 'BKPMIN'], axis=1, inplace=True)

        # ANALYZE:
        # fpogv (is the fixation pog valid)
        # (The valid flag with value of 1 (TRUE) if the fixation POG data is valid, and 0
        # (FALSE) if it is not. FPOGV valid is TRUE ONLY when either one, or both, of the
        # eyes are detected AND a fixation is detected. FPOGV is FALSE all other times, for
        # example when the subject blinks, when there is no face in the field of view,
        # when the eyes move to the next fixation (i.e. a saccade). )
        # when fpogx = 0, the row is dropped
        # -- Decided to leave it for now since rapid eye movements may be useful (saccade)

        # LPCX LPCY  (left eye pupil x and y  coords in cam img as fraction of cam img size)
        # RPCX RPCY  (right eye pupil x and y  coords in cam img as fraction of cam img size)

        # LPD/RPD (diameter of left/right eye pupil in pixels)

        # LPS/RPS (: The scale factor of the left/right eye pupil (unitless). Value equals 1 at calibration
        # depth, is less than 1 when user is closer to the eye tracker and greater than 1 when user
        # is further away.)

        # LPV/RPV (whether the left/right eye pupil info is correct

        # Correct:
        # (bkdur is the preceding blink duration)
        # bkid should be changed to either 0 for none or 1 for blinking

        # instead of returning an id, it returns 0 for no blink and 1 for a blink right now
        # data['BKID'] = np.where(data["BKID"] > 0, 1, 0)
        # REMOVED

        # # Calculating number of invalid rows -> [removed now]
        # print("Number of invalid rows FPOGV:")
        # print(data.groupby(by='FPOGV').count())
        # print("Number of invalid rows LPV:")
        # print(data.groupby(by='LPV').count())
        # print("Number of invalid rows RPV:")
        # print(data.groupby(by='RPV').count())
        # print("Number of invalid rows BPOGV:")
        # print(data.groupby(by='BPOGV').count())

        # # Dropping the rows with invalid data
        # data.drop(data[data['FPOGV'] < 1].index, inplace=True)
        # data.drop(data[data['LPV'] < 1].index, inplace=True)
        # data.drop(data[data['RPV'] < 1].index, inplace=True)
        # data.drop(data[data['BPOGV'] < 1].index, inplace=True)

        # # Calculating number of invalid rows -> [removed now]
        # print("Number of invalid rows FPOGV:")
        # print(data.groupby(by='FPOGV').count())
        # print("Number of invalid rows LPV:")
        # print(data.groupby(by='LPV').count())
        # print("Number of invalid rows RPV:")
        # print(data.groupby(by='RPV').count())
        # print("Number of invalid rows BPOGV:")
        # print(data.groupby(by='BPOGV').count())

        # Dropping the columns that determined invalid data (not needed anymore)
        data.drop(['FPOGV', 'LPV', 'RPV', 'BPOGV'], axis=1, inplace=True)

        # COMBINING INFO
        data['LPDLPS'] = np.where(True, data['LPD']*data['LPS'], 0)
        data['RPDRPS'] = np.where(True, data['RPD']*data['RPS'], 0)

        # Dropping unused columns
        data.drop(['LPD', 'LPS', 'RPD', 'RPS'], axis=1, inplace=True)

        print(f"Saving {pathStr}")
        data.to_csv(pathStr, index=False)
        return data


if __name__ == "__main__":
    ECGDataCleaner().main()
