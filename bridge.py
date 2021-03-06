import os
import sys
from django.core.wsgi import get_wsgi_application
proj_path = "./mud_py"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mud_py.mud_py.mud_py.settings')
sys.path.append(proj_path)
os.chdir(proj_path)

application = get_wsgi_application()

from sensor.models import Sensor

s = Sensor (sensorID = 'Test')
s.save()
