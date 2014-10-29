import logging


class Logger(object):
    """
    Generic logging class
    """

    def __init__(self, filename):
        self.filename = filename

    def setup(self):
        logging.basicConfig(
            format='%(asctime)s %(filename)-12s %(levelname)-8s %(message)s',
            level=logging.DEBUG)
        return logging.getLogger(self.filename)
