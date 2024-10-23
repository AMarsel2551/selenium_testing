import logging

LOGGING_LEVEL = 'info'

LOGGING_LEVEL = LOGGING_LEVEL.upper()

level = logging.WARNING
if hasattr(logging, LOGGING_LEVEL):
    level = getattr(logging, LOGGING_LEVEL)

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger(__name__)
log.setLevel(level)

log.debug(f"Got logging level {LOGGING_LEVEL} at module {__name__}")
