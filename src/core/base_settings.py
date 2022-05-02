import logging
from os import environ

from dotenv import load_dotenv

load_dotenv()

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 1

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

LOG_ENABLED = 1
LOG_LEVEL = logging.INFO

#

REDIS_URL = environ.get("REDIS_URL", "")
