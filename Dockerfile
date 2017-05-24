FROM karimtabet/wagtailalpine:latest

ENV PAPUSA_SRVHOME=/srv
ENV PAPUSA_SRVPROJ=/srv/papusa

RUN mkdir /srv/logs

COPY app/ /srv/papusa/app/
COPY papusa/ /srv/papusa/papusa/
COPY manage.py entrypoint.sh /srv/papusa/

WORKDIR /srv/papusa
CMD ["./entrypoint.sh"]
