import constants

bind = '0.0.0.0:' + str(constants.PORT_NUMBER)
worker_class = 'uvicorn.workers.UvicornWorker'
accesslogformat = '%(h)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = constants.LOG_PATH
errorlog = constants.ERROR_LOG_PATH
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True
