import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

handler = logger.handlers and logger.handlers[0] or logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s [%(filename)s:%(lineno)s] %(message)s'))
if not logger.handlers:
    logger.addHandler(handler)
