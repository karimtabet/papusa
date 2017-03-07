############################################################
# Dockerfile to set up Papusa project
# Based on an Ubuntu Image
# Installs Python and Pip
# Creates media and logs volumes
# Installs Python dependencies
# Exposes port 8000
# Calls entrypoint
############################################################

FROM ubuntu:16.04

MAINTAINER Karim Tabet

ENV PAPUSA_SRVHOME=/srv
ENV PAPUSA_SRVPROJ=/srv/papusa

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip
RUN pip install --upgrade pip

WORKDIR $PAPUSA_SRVHOME
RUN mkdir media static logs
VOLUME ["$PAPUSA_SRVHOME/media/", "$PAPUSA_SRVHOME/logs/"]

COPY ./ $PAPUSA_SRVPROJ

RUN pip install -r $PAPUSA_SRVPROJ/requirements.txt

EXPOSE 8000

WORKDIR $PAPUSA_SRVPROJ
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
