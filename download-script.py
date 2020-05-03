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

op = input("options[1]:\n1.clone all\n2.clone seleceted\n3.ignore selected: ")
if (op == "\n"):
    op = 1


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

        except git.exc.GitCommandError as e:
            print('not an empty directory\ntrying to pull from master')


def downloadAll():
    download()


def downloadSelected():
    download()


def ignoreSelected():
    download()
