#
# Build a simple ubuntu container and load our django web app
#
FROM ubuntu:latest
MAINTAINER Noel Wilson "jwnwilson@hotmail.co.uk"

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update
RUN apt-get install -y python python-pip wget
RUN apt-get install -y git python-virtualenv
RUN apt-get install -y python-dev
RUN apt-get install -y libpq-dev

# Left as reference for working with private repositories later
# Make ssh dir
#RUN mkdir /root/.ssh/
# Copy over private key, and set permissions
#ADD id_rsa /root/.ssh/id_rsa
# Create known_hosts
#RUN touch /root/.ssh/known_hosts
# Add bitbuckets key
#RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

WORKDIR /home

# Create venv
RUN virtualenv venv

# Clone the master branch into /home run if $DEV != 1
RUN git clone https://github.com/jwnwilson/twitter_bot.git
RUN source /home/venv/bin/activate;pip install -r /home/twitter_bot/requirements.txt
RUN chmod 755 /home/twitter_bot/shell_scripts/run_server.sh

# Append virtual env source to .bashrc
echo "# Source virtual env on shell shartup" >> /root/.bashrc
echo "source /home/venv/bin/activate" >> /root/.bashrc

# Port to expose
EXPOSE 8000
EXPOSE 8080




