FROM python:3.6-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY . /app
WORKDIR /app

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

RUN chmod +x ./devops/run.sh

EXPOSE 5000
ENTRYPOINT ["./devops/run.sh"]
