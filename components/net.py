from time import time, sleep

from psutil import net_io_counters

from components.template import TemplateListener


class NetListener(TemplateListener):

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
            data = net_io_counters()

            # Publish stats for every data
            self.mqtt_client.publish("cabackend/netpacketssent_01", data[2])
            self.mqtt_client.publish("cabackend/netpacketsreceived_01", data[3])

            # Check if stop
            if self.kill:
                print("NetListener returning...")
                return 0
            sleep(max(0.0, start_time - time()))
