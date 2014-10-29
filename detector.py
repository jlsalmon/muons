#!/usr/bin/python
from __future__ import print_function

from XRootD.client.flags import OpenFlags
from XRootD import client

from sensors import adc
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
        self.adc_module = adc.ADC(0, self)

        self.filesystem = client.FileSystem("root://localhost//tmp")
        self.create_event_file()

    def run(self):
        """
        Main function that will load all the necessary modules and start
        taking data.
        """
        self.log.info("Running muon detector")

        self.gps_module.start()
        self.adc_module.start()

        self.gps_module.join()
        self.adc_module.join()

    def on_event(self, data):
        """
        Do something when we get an event from the ADC
        """
        event = Event(data, self.gps_module.current_timestamp,
                      self.gps_module.current_lat,
                      self.gps_module.current_lon)

        self.log.debug("Got response from ADC: %s" % event)

        # Dump the event to a file
        print(str(event), file=open('/tmp/event.txt', 'a'))

    def on_gpgga(self, gpgga):
        """
        Do something when we get a GPS pulse
        """
        self.log.debug("on_gpgga()")

    def create_event_file(self):
        """
        Creates an event file in the xrootd filesystem (if it doesn't exist)
        """
        status, statinfo = self.filesystem.stat("/tmp/event.txt")
        if statinfo is None:
            with client.File() as f:
                f.open("root://localhost//tmp/event.txt", OpenFlags.NEW)


class Event(object):
    def __init__(self, data, timestamp, lat, lon):
        self.data = data
        self.timestamp = timestamp
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "data=%s time=%f lat=%f long=%f" % (self.data,
                                                   self.timestamp,
                                                   self.lat,
                                                   self.lon)


def main():
    muon_detector = MuonDetector()
    muon_detector.run()

# Bootstrap
if __name__ == '__main__':
    main()

