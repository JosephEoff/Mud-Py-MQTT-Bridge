import paho.mqtt.client as mqtt #import the client1
import time

topicFieldSeparator = '/'

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    
def on_node_message(client, userdata, message):
    print("Node Message")
    print("message received " ,str(message.payload.decode("utf-8")))
    fields = splitNodeTopicToFields(message.topic)
    print ('Node ID=', fields.ID)
    print ('Node DataType=', fields.DataType)
    #print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def splitNodeTopicToFields(topic):
    fields = topic.split(topicFieldSeparator)
    if not len(fields) == 3:
        raise ValueError
    return NodeFields(fields[1],fields[2])
    
class NodeFields():
    def __init__(self, ID, DataType):
        self.ID = ID
        self.DataType = DataType
    
    

broker_address="192.168.0.2" #Address needs to be a configuration setting.

nodeSubscription = 'node/#'

print("creating new instance")
client = mqtt.Client("MudPyBridge") #Name needs to be a configuration setting
client.on_message=on_message #attach function to callback
client.message_callback_add(nodeSubscription, on_node_message)
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","node")
client.subscribe(nodeSubscription)

while True:
    time.sleep(4) 
    pass

client.loop_stop() #stop the loop
