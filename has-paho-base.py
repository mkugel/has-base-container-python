import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import os

# micro service container defaults

id = 1
tier = 2
service_type = "safety"
service_name = "smoke-alarm"
broker_main = os.getenv('BROKER_MAIN', "192.168.1.101")

def publish_value(message_body):
    publish.single("information/service/safety/smoke-alarm/value", message_body, hostname=broker_main)

def power_off():
    print("Powering off")

def power_on():
    print("Powering on")

def health_beat():
    print("Health Beat")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("control/service/" + service_type + "/" + service_name + "/power")
    client.subscribe("information/service/" + service_type + "/" + service_name + "/value")
    client.subscribe("information/system/health")
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    msgs = [{'topic':"service/safety/dt-1", 'payload':"transformed"},
    ("service/safety/dt-1", str(msg.payload)[4:len(str(msg.payload))-2], 0, False)]
    publish.multiple(msgs, hostname=broker_main)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_main, 1883, 60)
client.loop_forever()
