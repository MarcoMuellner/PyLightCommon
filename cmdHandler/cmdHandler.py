import os
from json import load
from typing import Dict

from django.conf import settings
from django.http import HttpResponse
from django.apps import apps

def registerFunction():
    registry = {}
    def registrar(func):
        registry[func.__name__] = func
        return func
    registrar.all = registry
    return registrar

cmd = registerFunction()

class CmdHandler:

    def __init__(self):
        self.obligatoryCommands = {
            "commando":str,
            "response":str,
            "type":str,
        }
        self.optionalCommands = {
            "hooked_function":dict,
            "main_model":str,
            "fields":dict,
        }
        self.cmdDict = {}
        self.cmdFilePath = settings.CMDPATH

        for filename in os.listdir(self.cmdFilePath):
            tmpDict = self.readJsonFile(filename)
            self.cmdDict[tmpDict["commando"]] = tmpDict

    def readJsonFile(self,file:str) -> Dict:
        if os.path.exists(file):
            with open(file,'r') as f:
                cmdDict = load(f)[0]
            for key,value in cmdDict.items():
                if key not in self.obligatoryCommands.keys() and key not in self.optionalCommands.keys():
                    raise AttributeError(f"The definition of the key {key} in file {file} is not an available"
                                         f"command.")
                try:
                    if not isinstance(value,self.obligatoryCommands[key]):
                        raise AttributeError(f"The type for {key} must be {self.obligatoryCommands[key]}")
                except KeyError:
                    if not isinstance(value,self.optionalCommands[key]):
                        raise AttributeError(f"The type for {key} must be {self.obligatoryCommands[key]}")
            return cmdDict
        else:
            raise FileNotFoundError(f"File {file} was not found!")

    def inCmd(self, request:str) -> HttpResponse:
        cmdData = request.split("||")
        if cmdData[0] in self.cmdDict.keys() and self.cmdDict[cmdData[0]]["type"] == "in":
            if "hooked_function" in self.cmdDict[cmdData[0]].keys():
                for key,val in self.cmdDict[cmdData[0]]["hooked_function"].items():
                    if val in cmd.all.keys():
                        cmd.all[val]()







    def outCmd(self,cmd):
        pass

