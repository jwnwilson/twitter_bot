#!/usr/bin/env bash

# Super simple setup script if we are running the exercise on a clean VM
sudo easy_install pip
sudo pip install virtualenv
sudo pip install virtualenvwrapper
pip install -r requirements.txt