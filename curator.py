import time
from util.logger import Logger
import schedule


class DataCurator(object):
    """
    This program runs periodically and sends data to the central server.
    """
    def __init__(self):
        self.log = Logger(__name__).setup()

    def run(self):
        self.log.info("Running data curator")

        schedule.every().day.at("20:55").do(self.curate)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def curate(self):
        self.log.info("Curation job running...")


def main():
    data_curator = DataCurator()
    data_curator.run()

# Bootstrap
if __name__ == '__main__':
    main()
