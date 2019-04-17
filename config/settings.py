MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

PYTHON_PATH = ""
SCRIPT_PATH = ""

try:
    from .local_settings import *
except:
    pass
