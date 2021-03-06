FROM resin/rpi-raspbian

RUN apt-get update && \
    apt-get install -y python-pip && \
    apt-get install postgresql && \
    apt-get install python-psycopg2 && \
    apt-get install libpq-dev && \
    pip install paho-mqtt && \
    pip install spyrk

RUN mkdir /ingestor
COPY . /ingestor
CMD ["python", "-u", "/ingestor/main.py"]
