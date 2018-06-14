import time
import requests
from enum import Enum
import json
import logging
import os
from subprocess import Popen

from PyLightCommon.Globals import *


class RunnerType(Enum):
    Server = "PyLightServer"
    Client = "PyLightSupport"


logger = logging.getLogger(__name__)


def updater(rType: RunnerType, version: str):
    while True:
        time.sleep(1)
        data = requests.get(f"http://api.github.com/repos/muma7490/{rType.value}/git/refs/tags")
        data = json.loads(data.text)[0]

        # checking if no tags available
        if keyMessage in data.keys():
            logger.debug("No tags available!")
            continue

        if keyNodeID in data.keys():
            url = data[keyURL]
            content = url.split("/")
            versionNew = content[-1]
            if compareVersions(version, versionNew):
                tagURL = f"https://github.com/muma7490/PyLightCommon/archive/{versionNew}.tar.gz"
                runScript(tagURL, versionNew, rType)
                return


def runScript(url, version, rType):
    logErr = open('updateScript_log_err.txt','w+')
    logStd = open('updateScript_log_std.txt','w+')
    script = f"{os.path.dirname(__file__)}/scripts/update_{'server' if rType == RunnerType.Server else 'client'}.sh {url} {version}"
    Popen(['nohup', script], stdout=logStd, stderr=logErr)


def compareVersions(versionOld: str, versionNew: str) -> bool:
    """
    Compares two versions with each other. Keeps to semantic versioning
    :param versionOld: Version to be compared against
    :param versionNew: New Version
    :return: True if version is newer, false if not
    """
    contentVersionOld = versionOld.split(".")
    contentVersionNew = versionNew.split(".")

    if len(contentVersionNew) != 3 or len(contentVersionOld) != 3:
        raise AttributeError(f"Contenversion have wrong format, expecting 3 items. Version old has "
                             f"{len(contentVersionOld)} items, Version new has {len(contentVersionOld)}"
                             f"items. Content version old is {contentVersionOld}, content version new is"
                             f"{contentVersionNew}")

    OldMajor = int(contentVersionOld[0].replace("v", ""))
    OldMinor = int(contentVersionOld[1])
    OldFix = int(contentVersionOld[2])

    NewMajor = int(contentVersionNew[0].replace("v", ""))
    NewMinor = int(contentVersionNew[1])
    NewFix = int(contentVersionNew[2])

    if NewMajor > OldMajor:
        return True
    elif NewMajor == OldMajor:

        if NewMinor > OldMinor:
            return True
        elif NewMinor == OldMinor:

            if NewFix > OldFix:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
