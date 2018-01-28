FROM python:3.4-alpine

EXPOSE 8000

ENV GUNICORN_CMD_ARGS --bind=0.0.0.0 --workers=2
ENV SECRET_KEY "override_this"
ENV DEBUG "False"
ENV SQLITE_PATH "/data/db.sqlite3"
ENV STATIC_URL "http://gionn.net/blood-reminders/assets/master/"

VOLUME [ "/data" ]

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "./startup.sh" ]