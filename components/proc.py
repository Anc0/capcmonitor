from time import time, sleep

from psutil import pids

from components.template import TemplateListener


class ProcListener(TemplateListener):

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

            proc_num = len(pids())

            # Query data from the os
            self.mqtt_client.publish("cabackend/procnum_01", proc_num)

            # Check if stop
            if self.kill:
                print("CpuListener returning...")
                return 0
            sleep(max(0.0, (start_time - time())))
