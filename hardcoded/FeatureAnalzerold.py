from datetime import datetime
import os.path as path
from typing import Tuple

import numpy as np
import pandas as pd

from DataGatherer import DataGatherer
from helper import Helper
from DataCleaner import DataCleaner
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from matplotlib import pyplot as plt
from logger import Logger
from CSVWriter import CSVWriter

from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, StackingClassifier


from DataSplitter import DataSplitter

# Not used
DIB_NAME = "DIB1"
DATASETS_PATH = path.join(DIB_NAME, 'dataRaw', 'ID')
SELECTED_DATA_SET_PATH = path.join("Single", "ET")
CONCAT_FILE_PATH = DIB_NAME
CONCAT_FILE_NAME = "concat-data"
CONCAT_FILE_EXT = ".csv"
CONCAT_FULLPATH_WITHOUT_EXT = path.join(CONCAT_FILE_PATH, CONCAT_FILE_NAME)

CSV_COLUMNS = ["Model"]

CSV_FORMAT = None


class FeatureAnalzerOld:
    def main(self):

        print("Getting initial clean data for csv column names")
        data: pd.DataFrame = DataCleaner().getCleanData(1)
        features, answers = DataSplitter().getAllFeaturesAndAnswers(data)
        CSV_COLUMNS.extend(features.columns.values.tolist())

        CSV_FORMAT = {CSV_COLUMNS[i]: i for i in range(len(CSV_COLUMNS))}

        for id in range(1, 29):

            print(f"Creating Logger with id:{id}")
            self.logger = Logger(
                f"features-nobk-macro-validOnly-test-{id}.txt")
            self.csvWriter = CSVWriter(
                f"features-nobk-macro-validOnly-test-{id}.csv", CSV_COLUMNS)

            self.logger.log("Getting clean data..")
            data: pd.DataFrame = DataCleaner().getCleanData(id)
            self.logger.log("Quick stats on clean data")
            Helper.quickDfStat(data)
            self.logger.log("Getting Data Sets..")
            features, answers = DataSplitter().getAllFeaturesAndAnswers(data)

            X_train, Y_train, X_val, Y_val, X_test, Y_test = DataSplitter().getTrainValTestSplit(data)
            self.logger.log(
                "Quick stats on features and answers for the train-val-test split")
            Helper.quickDfArrStat([X_train, Y_train])
            Helper.quickDfArrStat([X_val, Y_val])
            Helper.quickDfArrStat([X_test, Y_test])

            self.logger.log(
                "Verifying the features and answers for the sets add up")
            self.logger.log("Verifying X..")
            featureArr = []
            for df in [X_train, X_val, X_test]:
                val = round(len(df.index)/len(features.index), 3)
                featureArr.append(val)
                self.logger.log(f"{val}")

            self.logger.log("Verifying Y..")
            answerArr = []
            for df in [Y_train, Y_val, Y_test]:
                val = round(len(df.index)/len(answers.index), 3)
                answerArr.append(val)
                self.logger.log(f"{val}")

            self.logger.log("Adding up X")
            sum = 0
            for x in featureArr:
                sum += x
            self.logger.log(f"Sum: {sum}")
            self.logger.log("Adding up Y")
            sum = 0
            for y in answerArr:
                sum += y
            self.logger.log(f"Sum: {sum}")

            self.logger.log("Calculating classification numbers")
            self.logger.log(data.groupby(by='classifier').count())

            #######################

            classifierNames = [
                # "Nearest Neighbors (3)",
                # "Linear SVM (kernel='linear', C=0.025)",
                # "RBF SVM (gamma=2, C=1)",
                # "Gaussian Process (1.0 * RBF(1.0)",
                # "Decision Tree (max_depth=5)",
                # "Random Forest (max_depth=5, n_estimators=10, max_features=1)",
                # "Neural Net (alpha=1, max_iter=1000)",


                "AdaBoost",
                # "Naive Bayes",
                # "QDA",
                # "Nearest Neighbors",
                # "Linear SVM",
                # "RBF SVM",


                # "Gaussian Process",


                "Decision Tree",
                "Random Forest",
                # "Neural Net",
            ]

            classifiers = [
                # KNeighborsClassifier(3),
                # SVC(kernel="linear", C=0.025),
                # SVC(gamma=2, C=1),
                # GaussianProcessClassifier(1.0 * RBF(1.0)),
                # DecisionTreeClassifier(max_depth=5),
                # RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
                # MLPClassifier(alpha=1, max_iter=1000),


                AdaBoostClassifier(),
                # GaussianNB(),
                # QuadraticDiscriminantAnalysis(),
                # KNeighborsClassifier(),
                # SVC(kernel="linear", C=0.025),  ##
                # SVC(gamma=2, C=1),
                # SVC(), ##


                # SVC(),
                # GaussianProcessClassifier(),


                DecisionTreeClassifier(),
                RandomForestClassifier(),
                # MLPClassifier(),


                # KNeighborsClassifier(3),
                # SVC(kernel="linear", C=0.025),
                # SVC(gamma=2, C=1),
                # GaussianProcessClassifier(1.0 * RBF(1.0)),
                # DecisionTreeClassifier(max_depth=5),
                # RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
                # MLPClassifier(alpha=1, max_iter=1000),
                # AdaBoostClassifier(),
                # GaussianNB(),
                # QuadraticDiscriminantAnalysis(),
            ]

            #############################

            for i, classifier in enumerate(classifiers):

                self.logger.log(f"Building Model: {classifier} on id {id}")
                model = self.buildModel(X_train, Y_train, classifier)

                # get importance
                importance = model.feature_importances_

                # Setting initial row value
                row = [" "] * len(CSV_COLUMNS)
                row[CSV_FORMAT["Model"]] = classifierNames[i]


                # Summarize feature importance
                for featureIndex, score in enumerate(importance):
                    self.logger.log('Feature: %s, Score: %.5f' % (
                        features.columns.values[featureIndex], score))
                    row[CSV_FORMAT[features.columns.values[featureIndex]]] = score
                
                # Add current row 
                self.csvWriter.addRow(row)

                # # plot feature importance
                # fig, ax = plt.subplots(figsize=(30, 10))
                # ax.bar([x for x in range(len(importance))], importance)
                # self.logger.log(features.columns.values)
                # ax.set_xticks([x for x in range(len(importance))])
                # ax.set_xticklabels(labels=features.columns.values)
                # #plt.show()
                # plt.savefig(path.join("Figures", "feature-test-"+ datetime.now().strftime(R"%m-%d-%Y, %H-%M-%S") + ".png"), format='png', dpi=200)

    def buildModel(self, features: pd.DataFrame, answers: pd.DataFrame, classifier: StackingClassifier):
        # from tutorial: https://machinelearningmastery.com/calculate-feature-importance-with-python/

        # define the model
        model = classifier

        # fit the model
        model.fit(features, answers)

        return model


if __name__ == "__main__":
    FeatureAnalzerOld().main()
