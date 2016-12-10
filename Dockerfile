FROM resin/rpi-raspbian
RUN apt-get update && apt-get install -y python-pip && apt-get install sqlite3 && pip install paho-mqtt && pip install spyrk
RUN mkdir /ingestor
COPY . /ingestor
CMD ["python", "-u", "/ingestor/main.py"]
