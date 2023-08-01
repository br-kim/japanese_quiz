source /home/ec2-user/build/app/venv/bin/activate
echo "activate venv"
export PATH=$PATH:$HOME/build/app/venv/lib/python3.11/site-packages
echo "export PATH"
source /home/ec2-user/.bashrc
echo "source bashrc"

cd /home/ec2-user/build/app
echo "cd app"

echo $DATABASE_URL
echo "check DATABASE_URL"

log_dir="/home/ec2-user/log"

# 디렉토리가 존재하는지 확인하고 없으면 생성
if [ ! -d "$log_dir" ]; then
  mkdir -p "$log_dir"
fi

current_date=$(date +"%Y%m%dT%H%M%S")

log_date_dir="/home/ec2-user/log/$current_date"

# 디렉토리가 존재하는지 확인하고 없으면 생성
if [ ! -d "$log_date_dir" ]; then
  mkdir -p "$log_date_dir"
fi


gunicorn -b :8000 apps:app -k uvicorn.workers.UvicornWorker --access-logfile - > \
 /home/ec2-user/log/$log_date_dir/out.log 2> /home/ec2-user/log/$log_log_date_dir/err.log < /dev/null &
