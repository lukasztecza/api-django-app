FROM python:3.9.7-alpine3.14

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /app/

RUN pip install --upgrade pip \
    && apk add --no-cache postgresql-libs \
    && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    && pip install -r requirements.txt \
    && apk del .build-deps \
    && addgroup -g 1010 -S devgroup \
    && adduser -u 1010 -S -G devgroup devuser

COPY ./manage.py /app/
COPY ./source /app/source

USER devuser

EXPOSE 8000
