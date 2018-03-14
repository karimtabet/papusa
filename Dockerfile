FROM karimtabet/wagtailalpine:latest

ENV PAPUSA_SRVHOME=/srv
ENV PAPUSA_SRVPROJ=/srv/papusa

RUN mkdir /srv/logs

COPY app/ $PAPUSA_SRVPROJ/app/
COPY papusa/ $PAPUSA_SRVPROJ/papusa/
COPY tests/ $PAPUSA_SRVPROJ/tests/
COPY manage.py entrypoint.sh $PAPUSA_SRVPROJ/

COPY requirements.txt /
RUN pip3 install -r requirements.txt

WORKDIR /srv/papusa
CMD ["./entrypoint.sh"]
