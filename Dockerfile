FROM karimtabet/wagtailalpine:latest

ENV PAPUSA_SRVHOME=/srv
ENV PAPUSA_SRVPROJ=/srv/papusa

WORKDIR $PAPUSA_SRVHOME
RUN mkdir media static logs
VOLUME ["$PAPUSA_SRVHOME/media/", "$PAPUSA_SRVHOME/logs/"]

COPY app/ $PAPUSA_SRVPROJ/app/
COPY papusa/ $PAPUSA_SRVPROJ/papusa/
COPY manage.py entrypoint.sh requirements.txt $PAPUSA_SRVPROJ/

EXPOSE 8000

WORKDIR $PAPUSA_SRVPROJ
COPY ./entrypoint.sh /
CMD ["/entrypoint.sh"]
