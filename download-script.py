#!/bin/python3
import os
import sys
import json
import requests
import git

userName = input("Enter your github username: ")
response = requests.get("https://api.github.com/users/"+userName+"/repos")
repos = json.loads(response.text)

if (len(repos) == 2 and repos["message"] == "Not Found"):
    print("no user in that name found\nRun program again")
    exit(1)

###need to imple###
saveLoc = input("enter directory name to save in[" + os.getcwd() + "]: ")

if (saveLoc == "\n"):
    saveLoc = os.getcwd()

try:
    os.mkdir(saveLoc)
    print("folder created")

except OSError as e:
    print(e)
    exit(1)


except FileExistsError as e:
    print("folder exists")


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

        except git.exc.GitCommandError as e:
            print(e)
            # doGitPull = input('do a git pull origin master?[y/n]: ')
            # will implement this later

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
