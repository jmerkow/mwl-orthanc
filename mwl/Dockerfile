FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /requirements.txt

WORKDIR /app
RUN pip install -U pip

RUN pip install -r /requirements.txt

COPY ./app /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]