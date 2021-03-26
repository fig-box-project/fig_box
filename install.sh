# yum update
yum install screen
screen -S dev
yum install git
git clone https://github.com/normidar/my_fastapi
cd my_fastapi
yum install python3.8
python3.8 -m venv tutorial-env
source tutorial-env/bin/activate
pip3.8 install --upgrade pip
pip3.8 install --upgrade setuptools
pip3.8 install -r requirements.txt