import paho.mqtt.client as mqtt 
import sys

nodeid = sys.argv[1]
nodevaluetype = sys.argv[2]
nodevalue = sys.argv[3]

broker_address="192.168.0.2" 
#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("MudPyNodeSimulator") #create new instance
client.connect(broker_address) #connect to broker
client.publish('mud-py-node/' + nodeid + '/' + nodevaluetype,nodevalue)#publish
