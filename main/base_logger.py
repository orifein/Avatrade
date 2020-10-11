import logging


class BaseLogger():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)


    def create_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)      
        logger.level = logging.DEBUG
        return logger
