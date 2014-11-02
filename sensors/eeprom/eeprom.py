from util import logger

log = logger.Logger(__name__).setup()

import RPi.GPIO as GPIO

def get_id():
    """
    Helper class to read the node ID from the EEPROM chip
    """
    # Use a dummy value for now
    # id = 10
    #
    # log.info("Got node id: %d", id)
    # return id

    GPIO.setmode(GPIO.BCM)
    a = 27
    b = 28

    GPIO.setup(a, GPIO.IN)
    GPIO.setup(b, GPIO.IN)

    x = GPIO.input(a)
    y = GPIO.input(b)

    print x, y

    return 10
