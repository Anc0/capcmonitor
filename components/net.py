from time import time, sleep

from psutil import net_io_counters

from components.template import TemplateListener
from config.settings import TOPIC_CONFIGURE, TOPIC_DATA


class NetListener(TemplateListener):

    def __init__(self, sampling_rate, mqtt_client):
        TemplateListener.__init__(self)

        self.sampling_rate = sampling_rate / 1000
        self.mqtt_client = mqtt_client

    def run(self):
        """
        Periodically (according to the sampling rate) sample relevant memory data.
        """
        self.mqtt_client.publish(TOPIC_CONFIGURE + "sensor", "netr_01")
        self.mqtt_client.publish(TOPIC_CONFIGURE + "sensor", "nets_01")

        while True:
            # Query data from the os
            data = net_io_counters()

            # Publish stats for every data
            self.mqtt_client.publish(TOPIC_DATA + "nets_01", data[2])
            self.mqtt_client.publish(TOPIC_DATA + "netr_01", data[3])

            # Check if stop
            if self.kill:
                print("NetListener returning...")
                return 0
            sleep(self.sampling_rate)
