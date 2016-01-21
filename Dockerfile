#
# Super simple example of a Dockerfile
#
FROM ubuntu:latest
MAINTAINER Noel Wilson "jwnwilson@hotmail.co.uk"

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update
RUN apt-get install -y python python-pip wget
RUN apt-get install -y git python-virtualenv
RUN apt-get install -y python-dev

# Make ssh dir
#RUN mkdir /root/.ssh/

# Copy over private key, and set permissions
#ADD id_rsa /root/.ssh/id_rsa

# Create known_hosts
#RUN touch /root/.ssh/known_hosts
# Add bitbuckets key
#RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

# Port to expose
EXPOSE 8000
EXPOSE 8080

WORKDIR /home

RUN virtualenv env

# Clone the conf files into the docker container
RUN git clone https://github.com/jwnwilson/twitter_bot.git
RUN source /home/env/bin/activate
RUN pip install /home/twitter_bot/requirements.txt



