import paho.mqtt.client as mqtt 
import sys
import local_settings as cfg

broker_address=cfg.broker_address

sensorid = sys.argv[1]
sensorvaluetype = sys.argv[2]
sensorvalue = sys.argv[3]

client = mqtt.Client("MudPySensorSimulator") #create new instance
client.connect(broker_address) #connect to broker
client.publish('mud-py-flora/' + sensorid + '/' + sensorvaluetype, sensorvalue)#publish
