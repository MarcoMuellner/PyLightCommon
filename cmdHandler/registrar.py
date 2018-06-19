from cmdHandler.cmdHandler import cmd

@cmd(name="temp1")
def func1():
    print("func1")

@cmd(name="temp2")
def func2():
    print("func2")