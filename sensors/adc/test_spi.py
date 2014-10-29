import time

from spidev import spidev


# Main function
def main():
    # Set up SPI interface
    spi = spidev.SpiDev()
    spi.open(0, 0)

    # Read data continuously from sensor
    while True:
        resp = spi.xfer2([0x01, 0x02])
        print resp

        time.sleep(1)


# Bootstrap
if __name__ == '__main__':
    main()
