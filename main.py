import paho.mqtt.client as mqtt
import logging
from spyrk import SparkCloud
import OperationsScheduler
from dao.SensorDataAccessor import SensorDataAccessor
import Config

ACCESS_TOKEN = 'a520cd5bd34112b273fda91b1164f011b81fd2de'

logging.basicConfig()
Logger = logging.getLogger(__name__)
Logger.setLevel(20)

pgConnection = Config.Configuration().getDatabaseConnection()
sensorDao = SensorDataAccessor(pgConnection)

def on_connect(client, userdata, flags, rc):
    Logger.info("Connected to mosquitto at host " + Config.Configuration().mqttHost)


def getReadingsAndPublish(args):
    client = args[0]
    spark = args[1]
    sensors = sensorDao.getAll()
    for sensor in sensors:
        try:
            value = spark.devices[sensor["name"]].read()
            jsonString = "{\"id\": " + str(sensor["id"]) + ",\"device_id\": \"" + sensor["device_id"] + "\",\"value\": " + str(value) + "}"
            Logger.info("Publishing to dionysus/moisture: " + jsonString)
            client.publish("dionysus/moisture", jsonString)
        except:
            Logger.error("Error: unable to get/publish reading from sensor " + sensor["name"] + ". Sensor may be offline.")

def main():

    sparkClient = SparkCloud(ACCESS_TOKEN)
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.connect(Config.Configuration().mqttHost, 1883, 60)

    OperationsScheduler.asyncRunAtInterval(getReadingsAndPublish, 1, (mqttClient, sparkClient), repeat=True)
    mqttClient.loop_forever()

main()
