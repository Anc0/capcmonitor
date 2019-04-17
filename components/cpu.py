from time import time, sleep

from psutil import cpu_percent

from components.template import TemplateListener


class CpuListener(TemplateListener):

    def __init__(self, sampling_rate, mqtt_client):
        TemplateListener.__init__(self)

        self.sampling_rate = sampling_rate / 1000
        self.mqtt_client = mqtt_client

    def run(self):
        """
        Periodically (according to the sampling rate) sample relevant cpu data.
        """
        start_time = time()
        while True:
            start_time += self.sampling_rate

            # Query data from the os
            data = cpu_percent(percpu=True)

            # Publish stat for every data
            i = 1
            for core in data:
                self.mqtt_client.publish("cabackend/cpuusage_0{}".format(i), core)
                i += 1

            # Check if stop
            if self.kill:
                print("CpuListener returning...")
                return 0
            sleep(max(0.0, (start_time - time())))
