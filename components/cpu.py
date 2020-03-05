from datetime import datetime
from time import time, sleep

from psutil import cpu_percent

from components.template import TemplateListener
from config.settings import TOPIC_CONFIGURE, TOPIC_DATA


class CpuListener(TemplateListener):

    def __init__(self, sampling_rate, mqtt_client):
        TemplateListener.__init__(self)

        self.sampling_rate = sampling_rate / 1000
        self.mqtt_client = mqtt_client

    def run(self):
        """
        Periodically (according to the sampling rate) sample relevant cpu data.
        """
        data = cpu_percent(percpu=True)
        i = 1
        for _ in data:
            self.mqtt_client.publish(TOPIC_CONFIGURE + "sensor", "cpu_{}".format(str(i).zfill(2)))
            i += 1

        while True:
            # Query data from the os
            data = cpu_percent(percpu=True)

            # Publish stat for every data
            i = 1
            for core in data:
                self.mqtt_client.publish(TOPIC_DATA + "cpu_{}".format(str(i).zfill(2)), core)
                i += 1

            # Check if stop
            if self.kill:
                print("CpuListener returning...")
                return 0

            sleep(self.sampling_rate)
