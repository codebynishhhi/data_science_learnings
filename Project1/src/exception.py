# whenever an exception gets raised throw this custom error message
import sys
import logging 

def error_message_detail(error, error_detail:sys):
    # variable exe_tb - extracted from built-in exc_info() ---> gives us the details like on which file the exception has 
    # occured, on which line number etc will be stored in exe_tb
    _,_,exc_tb = error_detail.exc_info()

    # get the filename where exception has occured
    filename = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error mesaage occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        filename, exc_tb.tb_lineno, str(error)
    
    )

    return error_message


# custom class to call the error_message_detail 
class CustomeException(Exception):
    def __init__(self, error_message, error_details):
        # inherit from the exception class
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_details)

    # print the error msg
    def __str__(self):
        return self.error_message
    

# to run any py file
if __name__ == "__main__":
    try:
        a= 1/0
    except Exception as e:
        logging.info("Divide by 0 error")
        raise CustomeException(e, sys)