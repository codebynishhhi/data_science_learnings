# We need data transformation to do EDA, Feature Engineering, data cleaning like converting
# categorical data to numerical data etc
# columnTransformer to create pipleline
# SimpleImputer - for finding missing values

import os
import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from src.exception import CustomeException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    # to save the model as a .pkl file
    preprocessor_ob_file_path = os.path.join('artifacts', "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    # function to create all the pkl files to convert all categorical data to numeric data
    def get_data_transformer_object(self):
        '''
        This function is respoinsible for data transformation - 
        1. Spliting the categorical and numerical features
        2. Creating categorical & numerical pipelines 
        3. Using CoulmnTransformer to combine both the pipelines
        4. Return preprocessor - the combined pipeline
        '''
        try:
            numerical_columns = ['reading score','writing score']
            categorical_columns = ['gender', 'race/ethnicity','parental level of education','lunch','test preparation course']

            # numerical pipeline to do process -
            # 1. to handle missing values using imputer(imputer handles missing values)
            # 2. to do standar scaler on the training data
            numerical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # categorical pipeline to do process -
            # 1. to handle missing values using imputer(imputer handles missing values)
            # 2. to do standar scaler on the training data
            # 3. OneHotEncoder() - to conver the categorical value st numerical values
            categorical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore")),  # returns sparse matrix by default
                    ("scaler", StandardScaler(with_mean=False))  # do not center sparse matrices
                ]
)
            logging.info("Numerical features standard scaling completed")
            logging.info("Categorical features encoding completed")


            # to combine both the numerical + categorical pipeline - CoulmnTransformer is used
            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, numerical_columns),
                    ("categorical_pipeline", categorical_pipeline, categorical_columns)

                ]
            )

            logging.info("Column Trnasformer executed successfully !")

            return preprocessor
            
        except Exception as e:
            raise CustomeException(e, sys)
    
    def initiate_data_transformation_process(self, train_path, test_path):
        ''' This function starts the transformation process'''
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train & test data completed")

            logging.info("Obtaining preprocessing object")

            # read all the preprocessor objects
            preprocessor_obj_data = self.get_data_transformer_object()

            target_column_name = "math score"
            numerical_columns = ['reading score','writing score']

            # drop target(output) column from input features
            # split input/ output features from data frame for both train & test data

            # for training data 
            input_features_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_train_feature_df = train_df[target_column_name]

            # for test data 
            input_features_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_test_feature_df = test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe & test dataframe")

            # fit & transform the trainig data
            input_features_train_arr = preprocessor_obj_data.fit_transform(input_features_train_df)
            input_features_test_arr = preprocessor_obj_data.transform(input_features_test_df)

            train_arr = np.c_[input_features_train_arr, np.array(target_train_feature_df)]
            test_arr = np.c_[input_features_test_arr, np.array(target_test_feature_df)]

            logging.info(f"Saved preprocessing object!")

            # save the pkl obj in the file path for pkl files
            save_object(
                file_path = self.data_transformation_config.preprocessor_ob_file_path,
                obj = preprocessor_obj_data
            )

            return(
                train_arr, test_arr, self.data_transformation_config.preprocessor_ob_file_path
            )
        except Exception as e:
            raise CustomeException(e, sys)


