#Twitter Bot

To Run

## setup
./setup.sh

## set environment vars:
export TWITTER_API_KEY='twitter_api_key'
export TWITTER_SECRET='twitter_secret'

## Start the server 
fab web

## Send post command and display results
fab hash_tag_battle:id=1


## Build docker compose
fab docker_compose:build=True

## Start docker compose
fab docker_compose
