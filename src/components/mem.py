from time import time, sleep

from psutil import virtual_memory

from src.components.template import TemplateListener


class MemListener(TemplateListener):

    def __init__(self, sampling_rate, mqtt_client):
        TemplateListener.__init__(self)

        self.sampling_rate = sampling_rate / 1000
        self.mqtt_client = mqtt_client

    def run(self):
        """
        Periodically (according to the sampling rate) sample relevant memory data.
        """
        start_time = time()

        while True:
            start_time += self.sampling_rate

            # Query data from the os
            data = virtual_memory()

            # Publish stats for every data
            self.mqtt_client.publish("cabackend/mempercentage_01", data[2])

            # Check if stop
            if self.kill:
                print("MemListener returning... Godobye, au revoir and auf wiedersehen.")
                return 0
            sleep(max(0.0, start_time - time()))
