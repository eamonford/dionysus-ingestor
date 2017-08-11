import paho.mqtt.client as mqtt
import logging
import OperationsScheduler
from dao.SensorDataAccessor import SensorDataAccessor
import Config
import json
import datetime

ACCESS_TOKEN = 'a520cd5bd34112b273fda91b1164f011b81fd2de'
SOURCE_TOPIC_NAME = "dionysus/moisture"
SINK_TOPIC_NAME = "dionysus/readings"

logging.basicConfig()
Logger = logging.getLogger(__name__)
Logger.setLevel(20)

pgConnection = Config.Configuration().getDatabaseConnection()
sensorDao = SensorDataAccessor(pgConnection)

def on_connect(client, userdata, flags, rc):
    Logger.info("Connected to mosquitto at host " + Config.Configuration().mqttHost)

def on_message(client, userdata, msg):
    try:
        messageDict = json.loads(str(msg.payload))
        sensor = sensorDao.getByDeviceId(messageDict["device_id"])[0]

        jsonBody = {
                        "metric": sensor["type"],
                        "time": datetime.datetime.now().isoformat(),
                        "value": messageDict["value"],
                        "battery": messageDict["battery"],
                        "device_id": messageDict["device_id"],
                        "name": sensor["name"]
                    }
        jsonString = json.dumps(jsonBody)
        Logger.info("Publishing to dionysus/moisture: " + jsonString)
        client.publish(SINK_TOPIC_NAME, jsonString)
    except IndexError as e:
        Logger.exception("Could not find sensor with this device ID in database. Message received from sensor was: " + msg.payload)
    except KeyError as e:
        Logger.exception("Could not parse message: " + msg.payload)
    except:
        Logger.exception("Unable to publish reading from sensor. Message received from sensor was: " + msg.payload)

def main():
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.connect(Config.Configuration().mqttHost, 1883, 60)
    mqttClient.subscribe(SOURCE_TOPIC_NAME)

    mqttClient.loop_forever()

main()
