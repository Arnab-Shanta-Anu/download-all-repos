#!/bin/python3
import os
import sys
import json
import requests
import git

username = input("Enter your github username: ")
response = requests.get("https://api.github.com/users/"+username+"/repos")
repos = json.loads(response.text)
print("totoal repos: ", len(repos))
i = 1
for repo in repos:

    print(i, ") " + repo["name"]+"\t")
    i += 1

op = input("options[1]:\n1.clone all\n2.clone seleceted\n3.ignore selected:")
if (op == "\n"):
    op = 1


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)
        restart_line()


def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()


for repo in repos:
    try:
        git.Repo.clone_from(repo["clone_url"],
                            repo["name"], progress=Progress())
        print("cloning ", repo["name"])

    except KeyError:
        print('some error')
