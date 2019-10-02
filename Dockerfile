# FROM ubuntu:16.04
FROM python:3.5
MAINTAINER silenceliang "l3754902@gmail.com"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]

