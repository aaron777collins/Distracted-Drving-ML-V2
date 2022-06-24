from typing import List, Tuple
import pandas as pd
import datetime

class HelperOld:

    @classmethod
    def printDf(self, df: pd.DataFrame, rows: int):
        print(df.head(rows))

    @classmethod
    def quickDfStat(self, df: pd.DataFrame):
        self.printDf(df, 5)
        print(df.shape)
        
    @classmethod
    def quickDfArrStat(self, dfs: List[pd.DataFrame]):
        for df in dfs:
            self.printDf(df, 5)
            print(df.shape)
            
    @classmethod
    def convertToFormattedTime(self, seconds: int) -> str:
        return str(datetime.timedelta(seconds=seconds))