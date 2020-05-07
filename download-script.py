#!/bin/python3
import os
import platform
import sys
import json
import requests
import git
from git.exc import GitCommandError

userName = input("Enter your github username: ")
response = requests.get("https://api.github.com/users/"+userName+"/repos")
repos = json.loads(response.text)

if (len(repos) == 2 and repos["message"] == "Not Found"):
    print("no user in that name found\nRun program again")
    exit(1)

seperator = ""
if (platform.system() == "Linux"):
    seperator = "/"

elif(platform.system() == "Windows"):
    seperator = "\\"

saveLoc = input("enter directory name to save in[" + os.getcwd() + "]: ")

if (saveLoc == "\n" or saveLoc == ""):
    saveLoc = os.getcwd()

temp = ""
x = saveLoc.split(seperator, 1)
if (x[0] == ""):
    temp = seperator
x = saveLoc.split(seperator)
saveLoc = ""
if (temp != ""):
    saveLoc = ""+seperator

for X in x:
    saveLoc = os.path.join(saveLoc, X)

try:
    if not os.path.exists(saveLoc):
        os.makedirs(saveLoc)

except OSError as e:
    print(e)
    exit(1)

print("saving in "+saveLoc)

print("totoal repos: ", len(repos))

numOfRepo = 1
for repo in repos:

    print(numOfRepo, ") " + repo["name"]+"\t")
    numOfRepo += 1


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line, end='')
        restart_line()


def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()


def download(downList):
    skipFlag = False
    if downList != "":
        skipFlag = True

    i = 0

    for repo in repos:
        i += 1
        if (skipFlag and (str(i) not in downList)):
            continue

        try:
            git.Repo.clone_from(repo["clone_url"],
                                saveLoc+"/"+repo["name"], progress=Progress())
            print("cloning ", repo["name"])

        except GitCommandError as e:
            print(e)
            doGitPull = input('do a git pull origin master?[y/n]: ')
            if (doGitPull == "y"):
                git.Repo(saveLoc + "/" + repo["name"]).remotes.origin.pull()
            elif (doGitPull == "n"):
                print("ignoring")
            else:
                print("not understood")

    return


def downloadAll():
    download("")
    return


def downloadSelected():
    inputStr = input("Enter the repo numbers to clone[eg: 1 2 3] : ")
    downList = inputStr.split()

    download(downList)
    return


def ignoreSelected():
    inputStr = input("Enter the repo numbers to ignore[eg: 1 2 3] : ")
    ignList = inputStr.split()

    downList = []

    for x in range(1, numOfRepo):

        if str(x) in ignList:
            continue

        downList.append(str(x))

    print(downList)
    download(downList)

    return


switcher = {
    1: downloadAll,
    2: downloadSelected,
    3: ignoreSelected
}

op = input(
    "options[1]:\n1.clone all\n2.clone seleceted\n3.ignore selected\n: ")

try:
    op = int(op)

except ValueError as e:
    op = 1

callFunc = switcher[op]
callFunc()
