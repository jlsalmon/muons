from abc import abstractmethod
import serial
from pynmea import nmea
import threading
import time
import sys
from util.logger import Logger

log = Logger(__name__).setup()

test = nmea.GPGGA()
test.parse("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47")


class GPS(threading.Thread):
    """
    Helper class to read GPS data in a separate thread.
    """

    def __init__(self, listener):
        log.info('Initialising GPS')
        super(GPS, self).__init__()
        self.daemon = True

        self.serial_port = serial.Serial("/dev/ttyAMA0", 9600, timeout=2)

        self.listener = listener
        self.current_timestamp = float(test.timestamp)
        self.current_lat = float(test.latitude)
        self.current_lon = float(test.longitude)

    def run(self):
        """
        Start reading GPS data from the UART. Updates will be sent to the
        callback function.
        """
        if not self.serial_port.isOpen():
            self.serial_port.open()

        if not self.serial_port.isOpen():
            log.fatal('Couldn\'t open serial port')
            sys.exit(-1)

        log.info('Serial port opened')
        log.info('GPS running')

        self.serial_port.flushOutput()
        self.serial_port.flushInput()

        while True:
            time.sleep(1)

            # Read from the UART
            line = self.serial_port.read(self.serial_port.inWaiting())

            self.serial_port.flushOutput()
            self.serial_port.flushInput()


            if line.startswith('$GPGGA'):
                gpgga = nmea.GPGGA()

                # Ask the object to parse the data
                gpgga.parse(line)

                # Set dummy timestamp
                self.current_timestamp = time.strftime("%H%M%S")
                # self.current_timestamp = float(gpgga.timestamp)

                self.current_lat = float(
                    float(gpgga.latitude[2:]) / 60) + float(gpgga.latitude[:2])
                self.current_lon = float(
                    float(gpgga.longitude[3:]) / 60) + float(
                    gpgga.longitude[:3])

                # Invoke the callback listener
                self.listener.on_gpgga(gpgga)


class GPSListener(object):
    """
    Defines the methods that should be implemented by a class wishing to
    receive updates from the GPS sensor.
    """

    @abstractmethod
    def on_gpgga(self, gpgga):
        """
        Called when the GPGGA sentence is updated
        """
        pass
