import paho.mqtt.client as mqtt 
import sys

sensorid = sys.argv[1]
sensorvaluetype = sys.argv[2]
sensorvalue = sys.argv[3]

broker_address="192.168.0.2" 
client = mqtt.Client("MudPySensorSimulator") #create new instance
client.connect(broker_address) #connect to broker
client.publish('mud-py-flora/' + sensorid + '/' + sensorvaluetype, sensorvalue)#publish
