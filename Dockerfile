############################################################
# Dockerfile to set up Papusa project
# Based on an Alpine Edge
# Install psycopg2 driver (no compiling in container)
# Installs Python and Pip
# Creates media and logs volumes
# Installs Python dependencies
# Exposes port 8000
# Calls entrypoint
############################################################

FROM alpine:edge

MAINTAINER Karim Tabet

ENV PAPUSA_SRVHOME=/srv
ENV PAPUSA_SRVPROJ=/srv/papusa

RUN apk update && \
  apk --update add python3-dev py3-psycopg2 py3-pillow \
  tiff-dev jpeg zlib-dev freetype lcms2 libwebp tcl tk python3-tkinter libxml2 libxslt \
  build-base

ENV LIBRARY_PATH=/lib:/usr/lib
  
RUN python3 -m ensurepip && \
  rm -r /usr/lib/python*/ensurepip

RUN pip3 install --upgrade pip setuptools && \
  rm -r /root/.cache

WORKDIR $PAPUSA_SRVHOME
RUN mkdir media static logs
VOLUME ["$PAPUSA_SRVHOME/media/", "$PAPUSA_SRVHOME/logs/"]

COPY app/ $PAPUSA_SRVPROJ/app/
COPY papusa/ $PAPUSA_SRVPROJ/papusa/
COPY manage.py entrypoint.sh requirements.txt $PAPUSA_SRVPROJ/

RUN pip3 install -r $PAPUSA_SRVPROJ/requirements.txt

EXPOSE 8000

WORKDIR $PAPUSA_SRVPROJ
COPY ./entrypoint.sh /
CMD ["/entrypoint.sh"]