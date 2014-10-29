from util import logger

log = logger.Logger(__name__).setup()


def get_id():
    """
    Helper class to read the node ID from the EEPROM chip
    """
    # Use a dummy value for now
    id = 10

    log.info("Got node id: %d", id)
    return id
