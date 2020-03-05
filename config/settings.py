DEVICE_ID = "92fb068a-5b57-479f-b34e-4c42b0702cc8"
DEVICE_NAME = "PC Monitor"

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

TOPIC_DATA = "data/" + DEVICE_ID + "/"
TOPIC_CONFIGURE = "configure/" + DEVICE_ID + "/"

PYTHON_PATH = ""
SCRIPT_PATH = ""

try:
    from .local_settings import *
except:
    pass

