import serial
import sys

serial_port = serial.Serial("/dev/ttyAMA0", 115200, timeout=2)

if not serial_port.isOpen():
    serial_port.open()

if not serial_port.isOpen():
    print 'Couldn\'t open serial port'
    sys.exit(-1)

print 'Serial port opened'
serial_port.flushOutput()
serial_port.flushInput()

while True:
    line = serial_port.read(serial_port.inWaiting())
    print 'received: ' + line
