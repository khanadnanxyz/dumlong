FROM python:3.6-alpine
ADD . /app
WORKDIR /app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python","app.py"]