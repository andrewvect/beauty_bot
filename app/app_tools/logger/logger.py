import logging


def log_error(error_message):
    logger = logging.getLogger('my_logger')

    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('../../my_log_file.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.error(error_message)


