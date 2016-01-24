#!/usr/bin/env bash
# Start interactive shell which can interact with postgres docker image
docker run -it -v ~/workspace/exercises/twitter_bot:/home/twitter_bot --link db:twitter_bot -e DOCKER=True  twitterbot_web