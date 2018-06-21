import os
from json import load
from typing import Dict
import requests

from django.conf import settings
from django.http import HttpResponse
from django.apps import apps
import importlib


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
            "commando": str,
            "response": str,
            "type": str,
        }
        self.optionalCommands = {
            "hooked_function": dict,
            "model": dict,
            "parameters": list,
            "method": str
        }

        self.modelCommands = {
            "name":str,
            "id":dict,
            "fields":dict
        }
        self.cmdDict = {}
        self.cmdFilePath = settings.CMDPATH

        self.loadJsonFiles(self.cmdFilePath)
        self.createCmdAwareness(settings.BASE_DIR)

    def createCmdAwareness(self,path):
        for root,dirs,files in os.walk(path):
            for file in files:
                if "cmd_tasks.py" == file:
                    file = root+f"/{file}"
                    moduleName = file.replace(settings.BASE_DIR+"/", "").replace(".py", "").replace("/",".")
                    importlib.import_module(moduleName)

    def loadJsonFiles(self,path):
        for filename in os.listdir(path):
            if '.json' in filename and 'cmd_' in filename:
                tmpDict = self.readJsonFile(path+f"/{filename}")
                self.cmdDict = {**self.cmdDict, **tmpDict}

    def readJsonFile(self, file: str) -> Dict:
        if os.path.exists(file):
            with open(file, 'r') as f:
                cmdDict = load(f)
            retDict = {}
            for i in cmdDict:
                cmdDict = self._validateDict(i)
                retDict[cmdDict["commando"]] = cmdDict
            return retDict
        else:
            raise FileNotFoundError(f"File {file} was not found!")

    def _validateDict(self,cmdDict):
        for key, value in cmdDict.items():
            if key not in self.obligatoryCommands.keys() and key not in self.optionalCommands.keys():
                raise AttributeError(f"The definition of the key {key} in file {file} is not an available"
                                     f"command.")
            try:
                if not isinstance(value, self.obligatoryCommands[key]):
                    raise AttributeError(f"The type for {key} must be {self.obligatoryCommands[key]}")
            except KeyError:
                if not isinstance(value, self.optionalCommands[key]):
                    raise AttributeError(f"The type for {key} must be {self.obligatoryCommands[key]}")

        if "model" in cmdDict.keys():
            for parameter,instanceType in self.modelCommands.items():
                if parameter not in cmdDict["model"].keys():
                    raise AttributeError(f"Parameter {parameter} has to be in modelcommands when using model!")

                if not isinstance(cmdDict["model"][parameter],instanceType):
                    raise AttributeError(f"Parameter {parameter} has to be of type {instanceType}")


        return cmdDict

    def inCmd(self, request: str) -> HttpResponse:
        cmdData = request.split("||")
        if cmdData[0] in self.cmdDict.keys() and self.cmdDict[cmdData[0]]["type"] == "in":

            if "model" in self.cmdDict[cmdData[0]].keys():
                app_name, model = self.cmdDict[cmdData[0]]["model"]["name"].split(".")
                model = apps.get_model(app_name, model)

                modelFilter = {}

                for key, val in self.cmdDict[cmdData[0]]["model"]["id"].items():
                    if val == "pk":
                        modelFilter[val] = int(cmdData[int(key)])
                    else:
                        modelFilter[val] = cmdData[int(key)]

                models = model.objects.filter(**modelFilter)

                if len(models) == 0:
                    modelInstance = model()
                else:
                    modelInstance = models[0]


                for key, val in self.cmdDict[cmdData[0]]["model"]["fields"].items():
                    setattr(modelInstance, val, cmdData[int(key)])

                modelInstance.save()

            if "hooked_function" in self.cmdDict[cmdData[0]].keys():
                for key, val in self.cmdDict[cmdData[0]]["hooked_function"].items():
                    if val in cmd.all.keys():
                        try:
                            functionString = "cmd.all[val]("
                            for param in key.split(","):
                                if functionString[-1] == "]":
                                    functionString +=","
                                functionString += f"cmdData[{param}]"
                            functionString += ")"
                            exec(functionString)
                        except IndexError:
                            raise IndexError(f"Failed to access item {key} in cmdData. Maybe commandstring to short?")
            return HttpResponse(self.cmdDict[cmdData[0]]["response"], content_type="text/plain")

    def outCmd(self, address: str, port: int, **kwargs):
        cmd = kwargs["commando"]
        if cmd in self.cmdDict.keys() and self.cmdDict[cmd]["type"] == "out":
            richCmd = cmd

            if "parameters" in self.cmdDict[cmd].keys():
                for parameter in self.cmdDict[cmd]["parameters"]:
                    richCmd += f"||{kwargs[parameter]}"

            if "model" in self.cmdDict[cmd].keys():
                app_name, model = self.cmdDict[cmd]["model"]["name"].split(".")
                model = apps.get_model(app_name,model)

                modelFilter = {}

                for key, val in self.cmdDict[cmd]["model"]["id"].items():
                    if val == "pk":
                        modelFilter[val] = int(kwargs[key])
                    else:
                        modelFilter[val] = kwargs[key]

                models = model.objects.filter(**modelFilter)

                if len(models) == 0:
                    modelInstance = model()
                else:
                    modelInstance = models[0]

                for key, val in self.cmdDict[cmd]["model"]["setValue"].items():
                    setattr(modelInstance, val, kwargs[key])

                modelInstance.save()

                for _,value in self.cmdDict[cmd]["model"]["fields"].items():
                    richCmd +=f"||{getattr(modelInstance,value)}"

            if self.cmdDict[cmd]["method"] == "get":
                response = requests.get(f"http://{address}:{port}/cmdHandler/", params={"comamndo": richCmd})
            elif self.cmdDict[cmd]["method"] == "post":
                response = requests.post(f"http://{address}:{port}/cmdHandler", data={"commando": richCmd})
            else:
                raise ValueError(f"Request type must be post or get. Method was {self.cmdDict[cmd]['method']}")

            if response.text != self.cmdDict[cmd]["response"]:
                raise IOError(
                    f"Response text {response.text} didn't match expected response {self.cmdDict[cmd]['response']}")
            return response
        return None


handler = CmdHandler()


def sendCommand(address="127.0.0.1", port="8000", **kwargs):
    handler.outCmd(address, port, **kwargs)
