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

current_date = $(date +"%Y%m%dT%H%M%S")
gunicorn -b :8000 apps:app -k uvicorn.workers.UvicornWorker > \
 /home/ec2-user/log/out_$current_date 2> /home/ec2-user/log/err_$current_date < /dev/null &
