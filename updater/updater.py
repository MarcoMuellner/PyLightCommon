import time
import requests
from enum import Enum

class RunnerType(Enum):
    Server = "PyLightServer"
    Client = "PyLightSupport"

def updater(rType: RunnerType, version: str):
    while True:
        time.sleep(5)
        data = requests.get(f"https://api.github.com/repos/muma7490/{rType.value}/git/refs/tags")
