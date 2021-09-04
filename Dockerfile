# pull the official docker image
FROM python:3.7.8-slim

# set work directory
WORKDIR /code

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 0
ENV TZ="Asia/Ho_Chi_Minh"

RUN apt-get update -y
RUN apt-get install -y libcairo2
RUN pip install poetry

COPY . /code/

# install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

EXPOSE 5000

CMD uvicorn main:app --host 0.0.0.0 --port 5000 --log-level debug --app-dir src --limit-concurrency 500 --limit-max-requests 500