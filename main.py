from argparse import ArgumentParser
from time import sleep

from paho.mqtt.client import Client

from components.cpu import CpuListener
from components.mem import MemListener
from components.net import NetListener
from components.proc import ProcListener
from config.settings import MQTT_HOST, PYTHON_PATH, SCRIPT_PATH, TOPIC_CONFIGURE, DEVICE_NAME


class PcMonitor:

    def __init__(self, sampling_rate=1000):
        self.sampling_rate = sampling_rate

        self.thread_delay = sampling_rate/1000/3
        self.mqtt_client = Client(client_id="pcmonitor")

        self.cpu_component = None
        self.mem_component = None
        self.net_component = None

    def run(self):
        """
        Initialize all listeners threads and execute them until an external signal.
        """
        print("Connecting to the mqtt broker...", end="")
        self.mqtt_client.connect(MQTT_HOST)
        print("DONE")

        print("Introuding to the system...", end="")
        self.mqtt_client.publish(TOPIC_CONFIGURE + "name", DEVICE_NAME)
        print("DONE")

        print("Initializing the components...", end="")
        self.cpu_component = CpuListener(1000, self.mqtt_client)
        self.mem_component = MemListener(1000, self.mqtt_client)
        self.net_component = NetListener(1000, self.mqtt_client)
        print("DONE")

        print("Running the components...", end="")
        self.cpu_component.start()
        sleep(self.thread_delay)
        self.mem_component.start()
        sleep(self.thread_delay)
        self.net_component.start()
        print("DONE")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.cpu_component.stop_thread()
            self.mem_component.stop_thread()
            self.net_component.stop_thread()

        return 0

    @staticmethod
    def generate_windows_script():
        """
        Generate .bat file that can be run on system startup.
        """
        with open("start_pcmonitor.bat", "w") as bat_file:
            bat_file.write(PYTHON_PATH + " " + SCRIPT_PATH + "\npause")

    @staticmethod
    def generate_linux_script():
        """
        Generate bash file that can be run on system startup.
        """
        with open("start_pcmonitor.sh", "w") as sh_file:
            sh_file.write("#!/bin/bash\n" + PYTHON_PATH + " " + SCRIPT_PATH)


if __name__ == "__main__":
    parser = ArgumentParser(description='Read program flags.')
    parser.add_argument('-w', dest='windows', action='store_true')
    parser.add_argument('-l', dest='linux', action='store_true')
    args = parser.parse_args()

    if args.windows:
        PcMonitor().generate_windows_script()
    elif args.linux:
        PcMonitor().generate_linux_script()
    else:
        monitor = PcMonitor()
        monitor.run()
