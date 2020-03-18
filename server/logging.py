# pylint: disable=missing-docstring
import logging
import logging.config
import datetime

LOG_FILENAME = datetime.datetime.now().strftime('_%Y_%m_%d.log')
DICT_LOG_CONFIG = {
    "version":1,
    "handlers":{
        "fileHandler":{
            "class":"logging.FileHandler",
            "formatter":"myFormatter",
            "filename":LOG_FILENAME
            }
        },
    "loggers":{
        "email-sender":{
            "handlers":["fileHandler"],
            "level":"INFO",
            }
        },
    "formatters":{
        "myFormatter":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    }

logging.config.dictConfig(DICT_LOG_CONFIG)

def get_logger(def_name):
    return logging.getLogger(def_name)
# LOG = logging.getLogger("email-sender")
# LOG.info("Program started")
