import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import os

# micro service identifiers

service_id = os.getenv('SERVICE_ID', 1)
service_tier = os.getenv('SERVICE_TIER', 1)
service_group = os.getenv('SERVICE_GROUP', 1)
service_version = os.getenv('SERVICE_VERSION', 1)
security_level = os.getenv('SECURITY_LEVEL', 1)
service_order = os.getenv('SERVICE_ORDER', 1)

# micro service labels

service_type = "climate"
service_name = "heating"
service_zone = "livingroom"
service_tag = "radiator"

# micro service environment

sensor_service_array = ["sensor-1" , "sensor-2" , "sensor-3" , "sensor-4"]
transform_service_array = ["dt-1" , "dt-2" , "dt-3" , "dt-4"]
gateway_service_array = ["gateway-1" , "gateway-2"]
data_service_array = ["dp-1" , "dp-2" , "dp-3"]
dashboard_service_array = ["dashboard-1" , "dashboard-2"]

# message broker

broker_main = os.getenv('BROKER_MAIN', "192.168.1.101")

# default function definitions

def publish_value(message_body):
    publish.single("information/service/safety/smoke-alarm/value", message_body, hostname=broker_main)

def power_off():
    print("Powering off")
    publish.single("information/service/log", "Powering off " + service_name, hostname=broker_main)   

def power_on():
    print("Powering on")
    publish.single("information/service/log", "Powering on " + service_name, hostname=broker_main)

def health_beat():
    print("Health Beat")
    publish.single("information/service/log", "Thump " + service_name, hostname=broker_main)

# Custom function definitions

def some_special_function():
    print("Doing something special")
    publish.single("information/service/log", "Special Message from " + service_name, hostname=broker_main)

def increase_temperature():
    print("Increasing Temperaure")
    publish.single("information/service/log", "Increasing temperature of " + service_name, hostname=broker_main)

def decrease_temperature():
    print("Decreasing Temperaure")
    publish.single("information/service/log", "Decreasing temperature of " + service_name, hostname=broker_main)

# Callbacks

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # The subscription to the following topics provides the message oriented interface

    # Service control

    client.subscribe("control/service/" + service_type + "/" + service_name + "/power")
    client.subscribe("control/service/" + service_type + "/" + service_name + "/tuning")

    # Service information

    client.subscribe("information/service/" + service_type + "/" + service_name + "/value")
    client.subscribe("information/service/" + service_type + "/" + service_name + "/availability")

    # System control

    client.subscribe("control/system/power")
    client.subscribe("control/system/tuning")

    # System information

    client.subscribe("information/system/health")
    client.subscribe("information/system/load")
    client.subscribe("information/system/status")
    client.subscribe("information/system/state")
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    msgs = [{'topic':"information/service/log", 'payload':str(msg.payload)},
    ("information/system/log", str(msg.payload), 0, False)]
    publish.multiple(msgs, hostname=broker_main)

    # messafe filtering

    if (msg.topic=="control/service/" + service_type + "/" + service_name + "/power"):
        if(msg.payload=="off"):
            power_off()
        elif(msg.payload=="on"):
            power_on()
    
    if (msg.topic=="control/service/" + service_type + "/" + service_name + "/tuning"):
        if(msg.payload=="increase"):
            increase_temperature()
        elif(msg.payload=="decrease"):
            decrease_temperature()

# Client Hook into Broker and Callbacks

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_main, 1883, 60)
client.loop_forever()
