import os 
import sys
import numpy as np
import pandas as pd
from src.exception import CustomeException
import pickle 
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        raise CustomeException(e, sys)