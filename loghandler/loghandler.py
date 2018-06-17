import os
import json
import logging.config

def setup_logging( default_path =  f"{os.path.dirname(__file__)}/logsettings.json", default_level=logging.DEBUG,):
    '''Setup logging configuration

    '''
    logging.getLogger("huey.contrib.djhuey.management.commands.run_huey").setLevel(logging.INFO)
    logging.getLogger("huey.contrib.djhuey.management.commands").setLevel(logging.INFO)
    logging.getLogger("huey.contrib.djhuey.management").setLevel(logging.INFO)
    logging.getLogger("huey.contrib.djhuey").setLevel(logging.INFO)
    logging.getLogger("huey.contrib").setLevel(logging.INFO)
    logging.getLogger("huey").setLevel(logging.INFO)
    logging.getLogger("requests").setLevel(logging.INFO)

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
