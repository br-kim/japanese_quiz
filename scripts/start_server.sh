export PATH=$PATH:$HOME/build/app/venv/lib/python3.9/site-packages
echo "export PATH"
source ~/.bashrc
echo "source bashrc"

cd /home/ec2-user/build/app
echo "cd app"
gunicorn -b :8000 apps:app -k uvicorn.workers.UvicornWorker
