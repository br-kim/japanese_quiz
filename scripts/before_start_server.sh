python3 -m venv /home/ec2-user/build/app/venv
echo "create venv"
source /home/ec2-user/build/app/venv/bin/activate
echo "activate venv"
pip install -r /home/ec2-user/build/app/requirements.txt
echo "install requirements"

