
from .models import Bidding

import json
import logging.config
import os
 
def setup_logging(default_path = "./conf/logging.json", default_level = logging.INFO, env_key = "LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path,"r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level = default_level)


setup_logging()
