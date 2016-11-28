import paho.mqtt.client as mqtt
from spyrk import SparkCloud
import OperationsScheduler
from dao.SensorDataAccessor import SensorDataAccessor
import sqlite3


ACCESS_TOKEN = 'a520cd5bd34112b273fda91b1164f011b81fd2de'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def getReadingsAndPublish(args):
    client = args[0]
    spark = args[1]

    sensors = SensorDataAccessor().getAll()
    for sensor in sensors:
        value = spark.devices[sensor["name"]].read()
        client.publish(
            "dionysus/moisture",
            "{device_id: " + sensor["device_id"] + ", value: " + str(value) + "}"
        )

def main():
    sparkClient = SparkCloud(ACCESS_TOKEN)

    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.connect("eamonford.hopto.org", 1883, 60)

    OperationsScheduler.asyncRunAtInterval(getReadingsAndPublish, 5, (mqttClient, sparkClient), repeat=True)
    mqttClient.loop_forever()


main()
