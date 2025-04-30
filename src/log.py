from pathlib import Path

import logging

from settings import settings

LOG_DIR = Path(__file__).parent.parent / Path('log')

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
LOG_DIR.mkdir(exist_ok=True)
log_file_path = LOG_DIR / Path('ToSScraper.log')
file_handler = logging.FileHandler(log_file_path)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)