import os
import json
import logging.config

def setup_logging( default_path = os.path.join('PyLightSupport/loghandler/logsettings.json'), default_level=logging.DEBUG,):
    '''Setup logging configuration

    '''
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print("BÄÄÄÄÄÄ")
        print(default_path)
        print(__name__)
        logging.basicConfig(level=default_level)
