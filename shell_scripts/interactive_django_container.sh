#!/usr/bin/env bash
# Start postgres deamon process
docker run --name db -d twitterbot_db
# Start interactive shell which can interact with postgres docker image
docker run --name web -p 8000:8000 -it -v ~/workspace/exercises/twitter_bot:/home/twitter_bot --link db:twitter_bot -e DOCKER=True  twitterbot_web  bash