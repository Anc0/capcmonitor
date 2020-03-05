from time import time, sleep

from psutil import virtual_memory

from components.template import TemplateListener
from config.settings import TOPIC_CONFIGURE, TOPIC_DATA


class MemListener(TemplateListener):

    def __init__(self, sampling_rate, mqtt_client):
        TemplateListener.__init__(self)

        self.sampling_rate = sampling_rate / 1000
        self.mqtt_client = mqtt_client

    def run(self):
        """
        Periodically (according to the sampling rate) sample relevant memory data.
        """
        self.mqtt_client.publish(TOPIC_CONFIGURE + "sensor", "mem_01")

        while True:
            # Query data from the os
            data = virtual_memory()

            # Publish stats for every data
            self.mqtt_client.publish(TOPIC_DATA + "mem_01", data[2])

            # Check if stop
            if self.kill:
                print("MemListener returning...")
                return 0
            sleep(self.sampling_rate)
