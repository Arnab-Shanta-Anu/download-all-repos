#!/bin/python3
import os
import json
import requests
import git

response = requests.get("https://api.github.com/users/arnab-shanta-anu/repos")
repos = json.loads(response.text)

class Progress(git.remote.RemoteProgress):
	def update(self, op_code, cur_count, max_count=None, message=''):
		print (self._cur_line)

for repo in repos:
	try:
		git.Repo.clone_from(repo["clone_url"], repo["name"], progress=Progress())
		print('cloning ' +repo["name"]+ ' into '+ os.getcwd()+'/'+repo["name"])
	except KeyError:
		print('some error')


