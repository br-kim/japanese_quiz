import constants
import os

bind = '0.0.0.0:' + str(constants.PORT_NUMBER)
worker_class = 'uvicorn.workers.UvicornWorker'
# access_log = constants.LOG_PATH
# error_log = constants.ERROR_LOG_PATH
logfile = constants.LOG_PATH+"gunicorn.log"
loglevel = 'info'
capture_output = True
