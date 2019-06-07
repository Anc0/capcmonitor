MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

PYTHON_PATH = ""
SCRIPT_PATH = ""

try:
    from .local_settings import *
except:
    pass
