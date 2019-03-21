FROM python:3.7.0-slim

ARG APP_VERSION_NAME=phrase-book-0.1

RUN mkdir -p /opt/${APP_VERSION_NAME}

RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/${APP_VERSION_NAME}

ADD . .

RUN pip install --no-cache-dir -r requirements.txt && python /opt/${APP_VERSION_NAME}/setup.py version

CMD [ "python", "/opt/phrase-book-0.1/app.py" ]