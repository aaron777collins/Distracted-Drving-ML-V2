from cgi import test
from datetime import datetime as dt
import os.path as path
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.gaussian_process.kernels import RBF

from DataGatherer import DataGatherer
from helper import Helper
from DataCleaner import DataCleaner
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, StackingClassifier
from matplotlib import pyplot as plt

from DataSplitter import DataSplitter
from logger import Logger
from ModelSaver import ModelSaver
from CSVWriter import CSVWriter, OUTPUT_FOLDER_PATH

GEN_NAME = "features-nobk-macro"

class CSVConcatOld:
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
    CSVConcatOld().main()