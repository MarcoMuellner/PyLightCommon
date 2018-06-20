import pytest
import os

from django.test import Client
from django.urls import reverse

from PyLightCommon.cmdHandler.cmdHandler import cmd,handler
from PyLightCommon.Commandos import *

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture(scope='module')
def moduleSetup(request):
    handler.loadJsonFiles(os.path.dirname(os.path.abspath(__file__)))
    return Client()

@pytest.mark.skip
@cmd
def testFunction1(param):
    print(f"TEST FUNCTION 1 {param}")

@pytest.mark.skip
@cmd
def testFunction2(param):
    print(f"TEST FUNCTION 2 {param}")

def test_get(moduleSetup : Client):
    response = moduleSetup.get(reverse("PyLightCommon.cmdHandler:commandHandler"),data={"commando":"testCommando||1||2||3"})
    assert response.status_code == 200
    assert response.content.decode() == "testResponse"


def test_post(moduleSetup : Client):
    response = moduleSetup.post(reverse("PyLightCommon.cmdHandler:commandHandler"),
                               data={"commando": "testCommando||1||2||3"})
    assert response.status_code == 200
    assert response.content.decode() == "testResponse"