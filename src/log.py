import logging

from settings import settings

class InvalidLogLevelError(Exception):
    pass

try:
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p:',
                        level=getattr(logging, settings['logLevel']))
except AttributeError:
    raise InvalidLogLevelError(
        f'The log level {settings['logLevel']} is invalid!'
    )

logger = logging.getLogger()
