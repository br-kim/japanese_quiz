source /home/ec2-user/build/app/venv/bin/activate
echo "activate venv"
export PATH=$PATH:$HOME/build/app/venv/lib/python3.11/site-packages
echo "export PATH"
source ~/.bashrc
echo "source bashrc"

cd /home/ec2-user/build/app
echo "cd app"
pip list

gunicorn -b :8000 apps:app -k uvicorn.workers.UvicornWorker
