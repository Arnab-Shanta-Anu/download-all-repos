#!/bin/bash
sudo apt update
sudo apt install python3 python3-pip git
pip3 install gitpython python-graphql-client
python3 download-script.py
