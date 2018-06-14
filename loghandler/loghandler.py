import os
import json
import logging.config

def setup_logging( default_path =  f"{os.path.dirname(__file__)}/logsettings.json", default_level=logging.DEBUG,):
    '''Setup logging configuration

    '''
    print(default_path)
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:

        print(default_path)
        print(__name__)
        logging.basicConfig(level=default_level)
