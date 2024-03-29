current_date=$(date +"%Y%m%dT%H%M%S")
JPN_QUIZ_DEPLOY_DATE=$current_date
export JPN_QUIZ_DEPLOY_DATE
LOG_PATH="/home/ec2-user/log/$JPN_QUIZ_DEPLOY_DATE/out.log"
ERROR_LOG_PATH="/home/ec2-user/log/$JPN_QUIZ_DEPLOY_DATE/err.log"

source /home/ec2-user/build/app/venv/bin/activate
echo "activate venv"
export PATH=$PATH:$HOME/build/app/venv/lib/python3.11/site-packages
echo "export PATH"
export JPN_QUIZ_ENVIRON=prod
echo "export JPN_QUIZ_ENVIRON"
export LOG_PATH
export ERROR_LOG_PATH
source /home/ec2-user/.bashrc
echo "source bashrc"

cd /home/ec2-user/build/app
echo "cd app"



log_dir="/home/ec2-user/log"

# 디렉토리가 존재하는지 확인하고 없으면 생성
if [ ! -d "$log_dir" ]; then
  mkdir -p "$log_dir"
fi


log_date_dir="/home/ec2-user/log/$current_date"

# 디렉토리가 존재하는지 확인하고 없으면 생성
if [ ! -d "$log_date_dir" ]; then
  mkdir -p "$log_date_dir"
fi

cd /home/ec2-user/build/app

alembic upgrade head
echo "alembic upgrade head"

#gunicorn apps:app -c gunicorn.conf.py --log-config gunicorn.logging.conf > $log_dir/$current_date/out 2> $log_dir/$current_date/err < /dev/null &

gunicorn apps:app -c gunicorn.conf.py --log-config gunicorn.logging.conf > /dev/null 2> /dev/null < /dev/null &


echo "start server"

echo "sleep 20"

sleep 20

response_code=$(curl -s -o /dev/null -w "%{http_code}" https://japanese-quiz.site/health)

if [ "$response_code" -ne 200 ]; then
    echo "Health check failed. Received response code: $response_code"
    exit 1
else
    echo "Health check succeeded. Received response code: $response_code"
fi

logrotate_conf="/etc/logrotate.d/jpn_quiz_logrotate"

cat << EOF > "$logrotate_conf"
$log_date_dir/err.log {
    su root ec2-user
    rotate 7
    daily
    missingok
    notifempty
    postrotate
      killall -s SIGUSR1 gunicorn
    endscript
}

$log_date_dir/out.log {
    su root ec2-user
    rotate 7
    daily
    missingok
    notifempty
    postrotate
      killall -s SIGUSR1 gunicorn
    endscript
}

EOF

chmod 644 "$logrotate_conf"

echo "create logrotate conf"

logrotate -f "$logrotate_conf"

echo "run logrotate"
