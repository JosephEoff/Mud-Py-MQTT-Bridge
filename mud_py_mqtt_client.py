#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import mud_py_API as MudPy
import datetime
import local_settings as cfg

topicFieldSeparator = '/'
broker_address=cfg.broker_address

nodeSubscription = 'mud-py-node/+/+'
sensorSubscription = 'mud-py-flora/+/+'
nodeBattery = 'battery'
nodeRSSI = 'rssi'
nodeDone = 'done'
nodeSleep = 'sleep'
nodeSensor = 'sensorID'
node = 'mud-py-node'


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    
def on_node_message(client, userdata, message):
    #The client receives the messages it sends.  Make sure to check the topic before handling a message
    try:        
        fields = splitTopicToFields(message.topic)
        
        #Nodes will always send a battery message first, so there's no need to create the node in the database for other messages.
        if fields.DataType == nodeDone:
            client.publish(node + '/' + fields.ID + '/' + nodeSleep,_getSecondsToNextHour() + 1800) #On the half hour
            return
        
        if fields.DataType == nodeRSSI :
            MudPy.updateNodeData(fields.ID, fields.DataType, str(message.payload.decode("utf-8")))
 
        if fields.DataType == nodeBattery:   
            MudPy.updateNodeData(fields.ID, fields.DataType, str(message.payload.decode("utf-8")))
            sensorIDs = MudPy.getSensorIDsForNode(fields.ID)
            for ID in sensorIDs:
                client.publish(node +'/' + fields.ID + '/' + nodeSensor,ID)
    except Exception as ex:
        print ('Method "on_node_message" :' + str(ex))
        print ('Method "on_node_message" :' + str(message.topic) + str(message.payload.decode("utf-8")))
    
        
def _getSecondsToNextHour():
    delta = datetime.timedelta(hours=1)
    now = datetime.datetime.now()
    next_hour = (now + delta).replace(microsecond=0, second=0, minute=0)

    return (next_hour - now).seconds   
    
def on_sensor_message(client, userdata, message):
    try:
        fields = splitTopicToFields(message.topic)
        MudPy.updateSensorData(fields.ID.upper(), fields.DataType, str(message.payload.decode("utf-8")))
    except Exception as ex:
         print ('Method "on_sensor_message" :' + str(ex))
         print ('Method "on_sensor_message" :' + str(message.topic) + str(message.payload.decode("utf-8")))
    

def splitTopicToFields(topic):
    fields = topic.split(topicFieldSeparator)
    if not len(fields) == 3:
        raise ValueError
    return NodeFields(fields[1],fields[2])
    
class NodeFields():
    def __init__(self, ID, DataType):
        self.ID = ID
        self.DataType = DataType
    

print("creating new instance")
client = mqtt.Client("MudPyBridge") #Name needs to be a configuration setting
client.on_message=on_message #attach function to callback
client.message_callback_add(nodeSubscription, on_node_message)
client.message_callback_add(sensorSubscription, on_sensor_message)
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
client.subscribe(nodeSubscription)
client.subscribe(sensorSubscription)

while True:
    time.sleep(0.1) 
    pass

client.loop_stop() #stop the loop
