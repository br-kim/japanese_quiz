export PATH=$PATH:$HOME/build/app/venv/lib/python3.9/site-packages
echo "export PATH"
source ~/.bashrc
echo "source bashrc"

gunicorn -b :8000 apps:app -k uvicorn.workers.UvicornWorker
