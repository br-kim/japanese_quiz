import constants

bind = '0.0.0.0:' + str(constants.PORT_NUMBER)
worker_class = 'uvicorn.workers.UvicornWorker'
workers=2
capture_output = True
enable_stdio_inheritance = True
