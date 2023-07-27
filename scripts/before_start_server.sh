python3.11 -m venv /home/ec2-user/build/app/venv
echo "create venv"

source /home/ec2-user/build/app/venv/bin/activate
echo "activate venv"

pip install -r /home/ec2-user/build/app/requirements.txt
echo "install requirements"

sudo systemctl start postgresql
echo "start postgresql"

sudo systemctl enable postgresql
echo "enable postgresql"

sudo systemctl start redis6
echo "start redis6"

sudo systemctl enable redis6
echo "enable redis6"