from time import time, sleep

import psutil
from psutil import pids, process_iter

from components.template import TemplateListener


class ProcListener(TemplateListener):

    def __init__(self, sampling_rate, mqtt_client):
        TemplateListener.__init__(self)

        self.sampling_rate = sampling_rate / 1000
        self.mqtt_client = mqtt_client
        self.pids = pids()

    def run(self):
        """
        Periodically (according to the sampling rate) sample relevant cpu data.
        """
        start_time = time()
        while True:
            start_time += self.sampling_rate

            current_pids = pids()

            if current_pids != self.pids:
                print("Process change detected.")
                previous_set = set(self.pids)
                current_set = set(current_pids)
                self.pids = current_pids

                print(previous_set - current_set)
                print(current_set - previous_set)

                # print(process_iter(attrs=['pid', 'name', 'username']))

                # for proc in process_iter():
                #     try:
                #         pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                #     except psutil.NoSuchProcess:
                #         pass
                #     else:
                #         print(pinfo)

            # Query data from the os
            # self.mqtt_client.publish("cabackend/procnum_01", proc_num)

            # Check if stop
            if self.kill:
                print("ProcListener returning...")
                return 0
            sleep(max(0.0, (start_time - time())))
