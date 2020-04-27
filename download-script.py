#!/bin/python3
import os
import json
import requests
from git import Repo

response = requests.get("https://api.github.com/users/arnab-shanta-anu/repos")
repos = json.loads(response.text)

for repo in repos:
	try:
		Repo.clone_from(repo["clone_url"],repo["name"])
		print('cloning ' +repo["name"]+ ' into '+ os.getcwd()+'/'+repo["name"])
	except KeyError:
		print('some error')


