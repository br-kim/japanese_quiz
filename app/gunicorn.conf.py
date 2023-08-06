import constants
import os

for key, value in os.environ.items():
    print(f'{key}: {value}')

bind = '0.0.0.0:' + str(constants.PORT_NUMBER)
worker_class = 'uvicorn.workers.UvicornWorker'
accesslog = f'/home/ec2-user/log/{os.getenv("JPN_QUIZ_DEPLOY_DATE")}/out.log'
errorlog = f'/home/ec2-user/log/{os.getenv("JPN_QUIZ_DEPLOY_DATE")}/err.log'
