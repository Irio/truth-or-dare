FROM python:3.6.2-alpine

RUN apk update && apk add --no-cache --virtual bash
# pandas dependencies: build-seps g++ python3-dev & the symlink command
RUN apk add --no-cache --virtual \
    build-deps \
    g++ \
    gcc  \
    python3-dev \
  && ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN adduser -S truth_or_dare
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

USER truth_or_dare
COPY . .