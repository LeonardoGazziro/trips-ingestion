import logging
from dynaconf import Dynaconf

# Create settings to get dynamic env vars.
settings = Dynaconf(
    settings_files=["settings.toml", ".secrets.toml"],
)

logger = logging.getLogger('Trips')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
