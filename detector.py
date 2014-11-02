#!/usr/bin/python
from __future__ import print_function

from XRootD.client.flags import OpenFlags
from XRootD import client
import json
import signal
import subprocess
import sys

from sensors import adc, temp, pressure
from sensors import gps
from sensors import eeprom
from util.logger import Logger


class MuonDetector(gps.GPSListener, adc.EventListener, object):
    """
    Main entry point into the muon detector program.
    """

    def __init__(self):
        self.log = Logger(__name__).setup()

        # Read our node ID
        self.node_id = eeprom.get_id()

        # Load the GPS module
        self.gps_module = gps.GPS(self)

        # Load the ADC module
        self.adc_module = adc.ADC(self)

        # Load the temperature and pressure sensors
        self.temp_module = temp.TemperatureSensor()
        self.pressure_module = pressure.PressureSensor()

        self.filesystem = client.FileSystem("root://localhost//tmp")
        self.create_event_file()

        # Register signal handler
        signal.signal(signal.SIGINT, self.signal_handler)

    def run(self):
        """
        Main function that will load all the necessary modules and start
        taking data.
        """
        self.gps_module.start()
        self.adc_module.start()

        self.log.info("Muon detector is running")

        # Wait until the process is killed
        signal.pause()

    def on_event(self, data, timestamp):
        """
        Do something when we get an event from the ADC
        """
        event = Event(self.node_id, data, timestamp,
                      self.gps_module.current_timestamp,
                      self.gps_module.current_lat,
                      self.gps_module.current_lon,
                      self.temp_module.read_temperature(),
                      self.temp_module.read_humidity(),
                      self.pressure_module.read_pressure())

        self.temp_module.read_firmware_version()
        self.log.debug("Got event from ADC: %s" % event)

        # Dump the event to a file
        print(json.dumps(event.__dict__), file=open('/tmp/event.txt', 'a'))

    def on_gpgga(self, gpgga):
        """
        Do something when we get a GPS pulse
        """
        self.log.debug("on_gpgga(): %s %s %s" % (gpgga.timestamp,
                                                 gpgga.latitude,
                                                 gpgga.longitude))

    def create_event_file(self):
        """
        Creates an event file in the xrootd filesystem (if it doesn't exist)
        """
        self.log.debug("Creating initial event file... (did you remember to "
                       "start xrootd? ;)")

        status, statinfo = self.filesystem.stat("/tmp/event.txt")
        if statinfo is None:
            with client.File() as f:
                f.open("root://localhost//tmp/event.txt", OpenFlags.NEW)

    def signal_handler(self, signal, frame):
        """
        Called when the process receives SIGINT
        """
        self.log.info('Received Ctrl-C')
        self.adc_module.cleanup()
        sys.exit(0)


class Event(object):
    def __init__(self, id=0, data=None, timestamp=0, gps_timestamp=0, lat=0,
                 lon=0, temperature=0, humidity=0, pressure=0):
        self.id = id
        self.data = data
        self.timestamp = timestamp
        self.gps_timestamp = gps_timestamp
        self.lat = lat
        self.lon = lon
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def __str__(self):
        return "id=%s data=%s timestamp=%s gps_timestamp=%s lat=%s long=%s " \
               "temperature=%s humidity=%s pressure=%s" % (
                   self.id,
                   self.data,
                   self.timestamp,
                   self.gps_timestamp,
                   self.lat,
                   self.lon,
                   self.temperature,
                   self.humidity,
                   self.pressure)


def main():
    muon_detector = MuonDetector()
    muon_detector.run()

# Bootstrap
if __name__ == '__main__':
    main()

