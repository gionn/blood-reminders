FROM python:3.4-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV GUNICORN_CMD_ARGS --bind=0.0.0.0 --workers=2

CMD [ "gunicorn", "blood.wsgi" ]