import logging

from constants import JPN_QUIZ_ENVIRON, LOG_PATH, ERROR_LOG_PATH

info_logger = logging.getLogger("fastapi_info_logger")
error_logger = logging.getLogger("fastapi_error_logger")

info_logger.setLevel(logging.INFO)
error_logger.setLevel(logging.ERROR)

console_info_handler = logging.StreamHandler()
console_info_handler.setLevel(logging.INFO)
console_error_handler = logging.StreamHandler()
console_error_handler.setLevel(logging.ERROR)

if JPN_QUIZ_ENVIRON == "test":
    info_logger.setLevel(logging.ERROR)
    info_logger.addHandler(console_info_handler)
    error_logger.addHandler(console_error_handler)
elif JPN_QUIZ_ENVIRON == "local":
    info_logger.addHandler(console_info_handler)
    error_logger.addHandler(console_error_handler)
elif JPN_QUIZ_ENVIRON == "prod":
    info_handler = logging.FileHandler(LOG_PATH)
    info_handler.setLevel(logging.INFO)

    error_handler = logging.FileHandler(ERROR_LOG_PATH)
    error_handler.setLevel(logging.ERROR)

    info_logger.addHandler(info_handler)
    error_logger.addHandler(error_handler)
