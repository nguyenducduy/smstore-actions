# pull official base image
FROM python:3.7.8-slim-stretch


ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 0
ENV TZ="Asia/Ho_Chi_Minh"

RUN apt-get update && apt-get install -y python-pip \
    && apt-get clean
RUN apt-get update ; apt-get install -y git build-essential gcc make yasm autoconf automake cmake libtool checkinstall libmp3lame-dev pkg-config libunwind-dev zlib1g-dev libssl-dev librdkafka-dev
RUN apt-get update \
    && apt-get clean \
    && apt-get install -y --no-install-recommends libc6-dev libgdiplus wget software-properties-common

RUN pip install poetry

# RUN wget https://www.ffmpeg.org/releases/ffmpeg-4.0.2.tar.gz
# RUN tar -xzf ffmpeg-4.0.2.tar.gz; rm -r ffmpeg-4.0.2.tar.gz
# RUN cd ./ffmpeg-4.0.2; ./configure --enable-gpl --enable-libmp3lame --enable-decoder=mjpeg,png --enable-encoder=png --enable-openssl --enable-nonfree
# RUN cd ./ffmpeg-4.0.2; make
# RUN  cd ./ffmpeg-4.0.2; make install

# set working directory
WORKDIR /code

# install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction


COPY ./src ./src

EXPOSE 5000

CMD uvicorn main:app --host 0.0.0.0 --port 5000 --log-level debug --app-dir src --limit-concurrency 3000 --limit-max-requests 3000