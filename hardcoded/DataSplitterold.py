import os.path as path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

TEST_SPLIT_PERCENT = 0.4
SEED = 42

class DataSplitterOld:
    # returns [features, answers]
    def getAllFeaturesAndAnswers(self, data:pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return [data.drop(['classifier'], axis=1), data['classifier']]
    
    #returns [X_train, Y_train, X_val, Y_val, X_test, Y_test]
    def getTrainValTestSplit(self, data:pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame,pd.DataFrame, pd.DataFrame]:
        features, answers = self.getAllFeaturesAndAnswers(data)
        
        X_train, X_test, Y_train, Y_test = train_test_split(features, answers, test_size=TEST_SPLIT_PERCENT, random_state=SEED)
        X_val, X_test, Y_val, Y_test = train_test_split(X_test, Y_test, test_size=0.5, random_state=SEED)
        return (X_train, Y_train, X_val, Y_val, X_test, Y_test)
        