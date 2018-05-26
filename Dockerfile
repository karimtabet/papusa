FROM alpine:edge

RUN apk update && \
  apk --update add python3-dev py3-psycopg2 py3-pillow \
  tiff-dev postgresql-dev zlib-dev jpeg freetype lcms2 \
  libwebp tcl tk python3-tkinter libxml2 libxslt \
  build-base

ENV LIBRARY_PATH=/lib:/usr/lib

RUN python3 -m ensurepip && \
  rm -r /usr/lib/python*/ensurepip

RUN pip3 install --upgrade pip setuptools && \
  rm -r /root/.cache

COPY requirements.txt /

RUN pip3 install -r requirements.txt

ENV PAPUSA_SRVHOME=/srv
ENV PAPUSA_SRVPROJ=/srv/papusa

RUN mkdir /srv/logs

COPY app/ /srv/papusa/app/
COPY papusa/ /srv/papusa/papusa/
COPY manage.py entrypoint.sh /srv/papusa/

WORKDIR /srv/papusa
CMD ["./entrypoint.sh"]
