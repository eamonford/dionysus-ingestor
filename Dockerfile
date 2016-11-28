FROM resin/rpi-raspbian
RUN apt-get update && apt-get install -y python-pip && apt-get install sqlite3 && pip install paho-mqtt && pip install spyrk
RUN mkdir /ingestor
COPY main.py /ingestor/main.py
COPY OperationsScheduler.py /ingestor/OperationsScheduler.py
COPY Config.py /ingestor/Config.py
COPY dao/ /ingestor/dao/
COPY db/ /ingestor/db/
RUN cd /ingestor && sqlite3 sensors.db < db/0.1_create_initial_tables.sql
CMD ["python", "/ingestor/main.py"]
