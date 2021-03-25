#!/usr/bin/env python3

import paho.mqtt.client as mqtt #import the client1
import time
import local_settings as cfg

broker_address=cfg.broker_address

############
def on_message(client, userdata, message):
    print("message topic=",message.topic)
    print("payload=" ,str(message.payload.decode("utf-8")))
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("")
########################################

#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("Snooper") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
client.subscribe("#")

while True:
    pass
time.sleep(4) # wait
client.loop_stop() #stop the loop
