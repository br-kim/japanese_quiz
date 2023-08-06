import constants

bind = '0.0.0.0:' + str(constants.PORT_NUMBER)
worker_class = 'uvicorn.workers.UvicornWorker'
workers = 2
accesslog = '/path/to/access.log'
errorlog = '/path/to/error.log'
