import sys
from enum import Enum


class EnumIOType(Enum):
    NONE = "IOType.NONE"
    OUTPUT =  "IOType.OUTPUT"
    INPUT = "IOType.INPUT"


from django.db import models

class ConnectedSystem(models.Model):
    name = models.CharField(max_length=255,verbose_name="Name of Client")
    lastIP = models.GenericIPAddressField(verbose_name="Last known IP address of client")
    lastMacAddress = models.CharField(max_length=255,verbose_name="Mac Address of client")
    serialNumber = models.CharField(max_length=255,verbose_name="Serial Number of Pi",unique=True)
    connected = models.BooleanField(default=False,verbose_name="Status of connection to pi")
    active = models.BooleanField(default=False,verbose_name="Status of Pi added in UI")

class IO(models.Model):
    ioNr = models.IntegerField(primary_key=True,verbose_name='physical io nr on pi')
    def getAllObjects(self):
        return IO.objects.all()

class IOType(models.Model):
    ioType = models.CharField(max_length=255, choices=[(tag,tag.value) for tag in EnumIOType], verbose_name="Type of output")
    def getAllObjects(self):
        return IOType.objects.all()

class UsedIO(models.Model):
    name = models.CharField(max_length=255,verbose_name='human readable name for the io')
    pin = models.ForeignKey(IO, on_delete=models.CASCADE, verbose_name='Pin nr')
    type = models.ForeignKey(IOType, on_delete=models.CASCADE, verbose_name='Type of IO')
    active = models.BooleanField(default=False,verbose_name="Active/Non Active IO")
    connectedSystem = models.ForeignKey(ConnectedSystem, on_delete=models.CASCADE)
    timeStart = models.TimeField(verbose_name="Start time of timer",null=True)
    timeEnd = models.TimeField(verbose_name="End time of timer",null=True)
