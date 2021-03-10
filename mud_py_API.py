import os
import sys
from django.core.wsgi import get_wsgi_application
from django.utils import timezone

proj_path = "./mud_py"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mud_py.mud_py.mud_py.settings')
sys.path.append(proj_path)
os.chdir(proj_path)

application = get_wsgi_application()

from sensor.models import Sensor
from sensor.models import SensorData
from sensor.models import SensorDataUnit
from sensor.models import SensorDataType
from controlnode.models import ControlNode
from controlnode.models import ControlNodeData
from controlnode.models import ControlNodeDataType
from controlnode.models import ControlNodeUnit

def updateNodeData(id, dataType, value):
    dType = _getNodeDataType(dataType)
    node = _getControlNode(id)
    data = ControlNodeData(node = node, datatype = dType, timestamp = timezone.now(), value = value)
    data.save()
    
def _getControlNode(id):
    node = None
    
    try:
        node = ControlNode.objects.get(nodeid = id)
    except ControlNode.DoesNotExist:
        node = ControlNode(nodeid = id)
        node.save()
        
    return node

def _getNodeDataType(dataType):
    dType = None
    
    try:
        dType = ControlNodeDataType.objects.get(typeName = dataType)
    except ControlNodeDataType.DoesNotExist:
        unit = _getUnitForNodeDataType(dataType)
        dType = ControlNodeDataType(typeName = dataType, unit = unit)
        dType.save()
        
    return dType

def _getUnitForNodeDataType(dataType):
    dUnitName = ''
    dUnitSymbol = ''
    
    if dataType == 'battery':
        dUnitName ='volts'
        dUnitSymbol = 'V'
    
    dUnit = None
    
    try:
        dUnit = ControlNodeUnit.objects.get(name = dataType)
    except ControlNodeUnit.DoesNotExist:
        dUnit = ControlNodeUnit(name = dUnitName, abbreviatedName = dUnitSymbol)
        dUnit.save()
        
    return dUnit

def updateSensorData(id,dataType, value):
    dtype = _getSensorDataType(dataType)
    sensor = _getSensor(id)
    data = SensorData(sensor = sensor, datatype = dtype, timestamp = timezone.now(), value = value)
    data.save()
        
def _getSensor(id):
    sensor = None
    
    try:
        sensor = Sensor.objects.get(sensorID = id)
    except Sensor.DoesNotExist:
        sensor = Sensor(sensorID = id)
        sensor.save()
        
    return sensor

def _getSensorDataType(dataType):
    dType = None
    
    try:
        dType = SensorDataType.objects.get(typeName = dataType)
    except SensorDataType.DoesNotExist:
        unit = _getUnitForSensorDataType(dataType)
        dType = SensorDataType(typeName = dataType, unit = unit)
        dType.save()
        
    return dType
    
def _getUnitForSensorDataType(dataType):
    dUnitName = ''
    dUnitSymbol = ''
    
    if dataType == 'battery':
        dUnitName ='percent'
        dUnitSymbol = '%'
    if dataType == 'moisture':
        dUnitName ='percent'
        dUnitSymbol = '%'
    if dataType == 'light':
        dUnitName ='lux'
        dUnitSymbol = 'lx'
    if dataType == 'temperature':
        dUnitName ='degrees'
        dUnitSymbol = '°C'
    if dataType == 'conductivity':
        dUnitName ='microsiemens per centimeter'
        dUnitSymbol = 'µS/cm'
    
    dUnit = None
    
    try:
        dUnit = SensorDataUnit.objects.get(name = dataType)
    except SensorDataUnit.DoesNotExist:
        dUnit = SensorDataUnit(name = dUnitName, abbreviatedName = dUnitSymbol)
        dUnit.save()
        
    return dUnit
