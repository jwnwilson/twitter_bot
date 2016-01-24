#!/usr/bin/env bash
if [ -f /home/twitter_bot/shell_scripts/twitter_env_var.sh ]
then
    source /home/twitter_bot/shell_scripts/twitter_env_var.sh
fi
# Activate venv
source /home/venv/bin/activate
python /home/twitter_bot/manage.py runserver 0.0.0.0:8000