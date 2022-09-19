# importing module
import logging
import os


class Log:

    def __init__(self) -> None:
        # Create and configure logger

        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # This is your Project Root
        log_file_path = ROOT_DIR + "/logs/log.log"
        logging.basicConfig(filename=log_file_path,format='%(asctime)s %(message)s',filemode='a')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def debug(self,message):
        self.logger.debug("Debug: "+ str(message))
    
    def info(self,message):
        self.logger.info("Info: "+ str(message))

    def warning(self,message):
        self.logger.warning( "Warning: "+ str(message))
 
    def error(self,message):
        self.logger.error("Error: "+ str(message))

    def critical(self,message):
        self.logger.critical("Critical: "+ str(message))
