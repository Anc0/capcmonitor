from time import sleep

from paho.mqtt.client import Client

from config.settings import MQTT_HOST
from src.components.cpu import CpuListener
from src.components.mem import MemListener
from src.components.net import NetListener


class PcMonitor:

    def __init__(self, sampling_rate=1000):
        self.sampling_rate = sampling_rate

        self.thread_delay = sampling_rate/1000/4
        self.mqtt_client = Client(client_id="pcmonitor")

        self.cpu_component = None
        self.mem_component = None
        self.net_component = None

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
        print("Components initialized.")

        print("Running the components...")
        self.cpu_component.start()
        self.mem_component.start()
        self.net_component.start()
        print("Components running.")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.cpu_component.stop_thread()
            sleep(self.thread_delay)
            self.mem_component.stop_thread()
            sleep(self.thread_delay)
            self.net_component.stop_thread()


if __name__ == "__main__":
    monitor = PcMonitor()
    monitor.run()
