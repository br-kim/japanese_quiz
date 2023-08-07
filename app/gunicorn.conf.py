import constants

bind = '0.0.0.0:' + str(constants.PORT_NUMBER)
worker_class = 'uvicorn.workers.UvicornWorker'
accesslog = constants.LOG_PATH+".access_log"
errorlog = constants.ERROR_LOG_PATH+".error_log"
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True
access_log_format = '%({x-real-ip}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
