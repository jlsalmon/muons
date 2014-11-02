from serial import Serial
import time

serialPort = Serial("/dev/ttyAMA0", 9600, timeout=2)
print 'baud: ', 9600

if (serialPort.isOpen() == False):
    serialPort.open()

if (serialPort.isOpen() == False):
    print 'Couldn\'t open serial port'

outStr = ''
inStr = ''

serialPort.flushInput()
serialPort.flushOutput()

for i, a in enumerate(range(33, 36)):
    outStr += chr(a)

    serialPort.write(outStr)
    time.sleep(1.0)
    inStr = serialPort.read(serialPort.inWaiting())

    print "inStr =  " + inStr
    print "outStr = " + outStr

    # if(inStr == outStr):
    #     print "WORKED! for length of %d" % (i+1)
    # else:
    #     print "failed"

serialPort.close()

