FROM python:3.9.9-alpine

WORKDIR /usr/src/coinmena

ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["./docker/web/entrypoint.sh"]