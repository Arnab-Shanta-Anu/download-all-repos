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

saveLoc = input("enter directory name to save in[" + os.getcwd() + "]: ")

if (saveLoc == "\n"):
    saveLoc = os.getcwd()

print("totoal repos: ", len(repos))
i = 1
for repo in repos:

    print(i, ") " + repo["name"]+"\t")
    i += 1


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line, end='')
        restart_line()


def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()


def download():
    for repo in repos:
        try:
            git.Repo.clone_from(repo["clone_url"],
                                repo["name"], progress=Progress())
            print("cloning ", repo["name"])

        except git.exc.GitCommandError:
            print('not an empty directory')
            # will implement later
            #doGitPull = input('do a git pull origin master?[y/n]: ')
    return


def downloadAll():
    # download()
    print("in download all")
    return


def downloadSelected():
    print("in sel download all")
    #inputStr = input("Enter the repo numbers to clone[eg: 1 2 3] : ")
    #downList = inputStr.split()

    # download()
    return


def ignoreSelected():
    # download()
    print("in ign download")
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
