from time import sleep

from paho.mqtt.client import Client

from components.cpu import CpuListener
from components.mem import MemListener
from components.net import NetListener
from components.proc import ProcListener
from config.settings import MQTT_HOST


class PcMonitor:

    def __init__(self, sampling_rate=1000):
        self.sampling_rate = sampling_rate

        self.thread_delay = sampling_rate/1000/4
        self.mqtt_client = Client(client_id="pcmonitor")

        self.cpu_component = None
        self.mem_component = None
        self.net_component = None
        self.proc_component = None

    def run(self):
        """
        Initialize all listeners threads and execute them until an external signal.
        """
        print("Connecting to the mqtt broker...")
        self.mqtt_client.connect(MQTT_HOST)
        print("Connection successful.")

        print("Initializing the components...")
        self.cpu_component = CpuListener(self.sampling_rate, self.mqtt_client)
        self.mem_component = MemListener(self.sampling_rate, self.mqtt_client)
        self.net_component = NetListener(self.sampling_rate, self.mqtt_client)
        self.proc_component = ProcListener(self.sampling_rate, self.mqtt_client)
        print("Components initialized.")

        print("Running the components...")
        self.cpu_component.start()
        sleep(self.thread_delay)
        self.mem_component.start()
        sleep(self.thread_delay)
        self.net_component.start()
        sleep(self.thread_delay)
        self.proc_component.start()
        print("Components running.")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.cpu_component.stop_thread()
            self.mem_component.stop_thread()
            self.net_component.stop_thread()
            self.proc_component.stop_thread()


if __name__ == "__main__":
    monitor = PcMonitor()
    monitor.run()
