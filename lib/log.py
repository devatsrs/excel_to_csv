# importing module
import logging


class Log:

    def __init__(self) -> None:
        # Create and configure logger
        logging.basicConfig(filename="./logs/log.log",format='%(asctime)s %(message)s',filemode='a')
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
