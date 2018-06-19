import os
import pytest

from cmdHandler.cmdHandler import cmd
from cmdHandler.cmdHandler import CmdHandler

@cmd
def testFunction1():
    pass

@cmd
def testFucntion2():
    pass


@pytest.fixture(scope='module')
def moduleSetup(request):
    return CmdHandler()

def testReadJsonFile(moduleSetup:CmdHandler):
    cmdDict = moduleSetup.readJsonFile(os.path.dirname(os.path.abspath(__file__))+"/testFile.json")