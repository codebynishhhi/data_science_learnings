import os
import sys
from src.exception import CustomeException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# any input that i require from any data scource will be give to this class
# @dataclass decorator to create & save variables
@dataclass
class DataIngestionConfig:
    # all the output of the injested data will be saved in this path in the artifact folder.
    # these all are the inputs that i am giving to the data injestion component 
    #  all the outputs will be saved in the respective files & path
    train_data_path:str = os.path.join('artifacts', "train.csv")
    test_data_path:str = os.path.join('artifacts', "test.csv")
    raw_data_path:str = os.path.join('artifacts', "data.csv")


# for funtions in our class
class DataInjestion:
    def __init__(self):
        # ingestion_config variable will have all the variables of DataIngestionConfig class
        self.ingestion_config = DataIngestionConfig()

    # read data from any db 
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method component")
        try:
            # read data from data source
            df = pd.read_csv('/Users/nishiigupta/Desktop/data_science_learnings/Project1/notebook/data/StudentsPerformance.csv')
            logging.info("read the dataset as data frame")

            # create the artifacts folder for training, test and raw data 
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # do the train test spilt and save the data in respective artifacts
            logging.info("train test split initated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # save data now after split
            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header = True)

            logging.info("ingestion of data completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomeException(e, sys)
        

if __name__ == "__main__":
    obj = DataInjestion()
    obj.initiate_data_ingestion()

