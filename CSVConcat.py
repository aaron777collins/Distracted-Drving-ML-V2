# Imports required modules for adding parents
import os.path as path
# import sys

# # Adds parent directory
# p = path.abspath('.')
# sys.path.insert(2, p)
# # Imports parent modules
# import ImportParentFiles
from EasyMLLib.logger import Logger
from EasyMLLib.CSVWriter import OUTPUT_FOLDER_PATH
import pandas as pd

from typing import List

GEN_NAME = "features-nobk-macro"

# ImportParentFiles.dummyFunc()

class CSVConcat:
    def main(self):
                
        # id = "concat"
        
        print("Creating Logger")
        self.logger = Logger(f"{GEN_NAME}-concat-csv.txt")
        
        dataArr: List[pd.DataFrame] = []
        
        for id in range(1, 29):
            csvName = f"{GEN_NAME}-{id}.csv"
            finalPath = path.join(OUTPUT_FOLDER_PATH, csvName)
            self.logger.log(f"Finding file at {finalPath}")
            
            if path.exists(finalPath):
                self.logger.log(f"{finalPath} found! Reading data..")
                data = pd.DataFrame(pd.read_csv(finalPath))
                data['ID'] = id
                dataArr.append(data)
            else:
                self.logger.log(f"ERROR!!!! Could not find {finalPath}")
                
        finalData = pd.concat(dataArr)
        
        finalData.to_csv(path.join(OUTPUT_FOLDER_PATH, GEN_NAME + "-concat-csv.csv"), index=False)

if __name__ == "__main__":
    CSVConcat().main()