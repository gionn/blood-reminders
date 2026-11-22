FROM python:3.14-alpine@sha256:5862d971d1f0ae26b258cefa4e893556b1d3aba81bd2ff30888704ad378bab67
EXPOSE 8000

ENV GUNICORN_CMD_ARGS=--bind=0.0.0.0 --workers=2
ENV DEBUG="False"
ENV SQLITE_PATH="/data/db.sqlite3"
ENV ADMIN_USERNAME="admin"
ENV ADMIN_EMAIL="admin@change.me"

VOLUME [ "/data" ]

WORKDIR /usr/src/app

RUN apk --update --no-cache add postgresql-libs musl-dev postgresql-dev gcc

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "./startup.sh" ]
