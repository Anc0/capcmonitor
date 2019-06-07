from time import time, sleep

from psutil import pids

from components.template import TemplateListener


class ProcListener(TemplateListener):

    def __init__(self, sampling_rate, mqtt_client):
        TemplateListener.__init__(self)

        self.sampling_rate = sampling_rate / 1000
        self.mqtt_client = mqtt_client
        self.pids = pids()

    def run(self):
        """
        Save process pids on every change.
        """
        # Save all pids that are running on program startup
        for pid in set(self.pids):
            self.mqtt_client.publish("cabackend/proc_01", str(pid) + "1")

        start_time = time()
        # Report on any new or killed pid.
        while True:
            start_time += self.sampling_rate
            current_pids = pids()

            if current_pids != self.pids:
                prev_set = set(self.pids)
                curr_set = set(current_pids)
                for pid in curr_set - prev_set:
                    self.mqtt_client.publish("cabackend/proc_01", str(pid) + "1")
                for pid in prev_set - curr_set:
                    self.mqtt_client.publish("cabackend/proc_01", str(pid) + "0")
                self.pids = current_pids

            # Check if stop
            if self.kill:
                for pid in self.pids:
                    # Without this delay, not all messages get sent
                    sleep(0.01)
                    self.mqtt_client.publish("cabackend/proc_01", str(pid) + "0")
                print("ProcListener returning...")
                return 0
            sleep(max(0.0, (start_time - time())))
