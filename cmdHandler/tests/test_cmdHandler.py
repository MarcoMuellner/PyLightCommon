import os
import pytest
import requests_mock
import requests
from django.conf import settings
from httmock import urlmatch,HTTMock

from PyLightCommon.cmdHandler.cmdHandler import cmd
from PyLightCommon.cmdHandler.cmdHandler import CmdHandler
from PyLightCommon.pylightcommon.models import ClientSettings

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.mark.skip
@cmd
def testFunction1(param):
    print(f"TEST FUNCTION 1 {param}")

@pytest.mark.skip
@cmd
def testFunction2(param):
    print(f"TEST FUNCTION 2 {param}")


@pytest.fixture(scope='module')
def moduleSetup(request):
    settings.CMDPATH = os.path.dirname(os.path.abspath(__file__))
    return CmdHandler()

def testReadJsonFile(moduleSetup:CmdHandler):
    cmdDict = moduleSetup.readJsonFile(os.path.dirname(os.path.abspath(__file__))+"/cmd_testFile.json")

def testCmdIn(moduleSetup:CmdHandler):
    ClientSettings(name="temp").save()
    moduleSetup.inCmd("testCommando||1||2||3")
    assert len(ClientSettings.objects.filter(name="2")) != 0
    assert len(ClientSettings.objects.filter(serverAddress="3"))

def testurl(requests_mock):
    requests_mock.get('http://test.com:8000', text='data')
    assert 'data' == requests.get('http://test.com:8000').text

def testCmdOut(moduleSetup:CmdHandler):
    @urlmatch(netloc=r'test\.com.+')
    def urlMock(url,request):
        return "testResponse2"

    with HTTMock(urlMock):
        moduleSetup.outCmd(address="test.com",port=8000
                           ,commando="testCommando2"
                           ,testParameter1="test1"
                           ,testParameter2="test2"
                           ,testParameter3="test3")