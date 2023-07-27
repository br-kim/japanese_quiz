python3 -m venv /home/ec2-user/build/app/venv
echo "create venv"
source /home/ec2-user/build/app/venv/bin/activate
echo "activate venv"
pip install -r /home/ec2-user/build/app/requirements.txt
echo "install requirements"
export PATH=$PATH:$HOME/build/app/venv/lib/python3.9/site-packages
echo "export PATH"
source ~/.bashrc
echo "source bashrc"
