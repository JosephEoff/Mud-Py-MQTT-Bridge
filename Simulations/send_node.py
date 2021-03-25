import paho.mqtt.client as mqtt 
import sys
import local_settings as cfg

broker_address=cfg.broker_address

nodeid = sys.argv[1]
nodevaluetype = sys.argv[2]
nodevalue = sys.argv[3]


#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("MudPyNodeSimulator") #create new instance
client.connect(broker_address) #connect to broker
client.publish('mud-py-node/' + nodeid + '/' + nodevaluetype,nodevalue)#publish
