#!/usr/bin/env bash
# Simple setup script to install temporary venv into project directory to make cleaning up easier
if [ ! -d ./venv ]
then
    sudo easy_install pip
    pip install virtualenv
    virtualenv venv
    # fabric so we can use fab commands
    pip install -r requirements.txt
fi

source /venv/bin/activate