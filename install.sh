# yes | source /install.sh
# git config --global credential.helper store

yum install -y git
yum install -y python3.8
# yum update
# 安装screen并安装dev
yum install -y epel-release
yum install -y screen
# screen -S dev
cd /
mkdir dev
cd /dev
git clone https://github.com/normidar/my_fastapi
cd my_fastapi
python3.8 -m venv tutorial-env
source tutorial-env/bin/activate
pip3.8 install --upgrade pip
pip3.8 install --upgrade setuptools
pip3.8 install -r requirements.txt
deactivate
# 安装puller
cd /
mkdir pull
cd /pull
git clone https://github.com/normidar/my_fastapi
cd my_fastapi
python3.8 -m venv tutorial-env
source tutorial-env/bin/activate
pip3.8 install --upgrade pip
pip3.8 install --upgrade setuptools
pip3.8 install -r requirements.txt
deactivate
# 安装oil
cd /
mkdir oil
cd /oil
git clone https://github.com/normidar/my_fastapi
cd my_fastapi
python3.8 -m venv tutorial-env
source tutorial-env/bin/activate
pip3.8 install --upgrade pip
pip3.8 install --upgrade setuptools
pip3.8 install -r requirements.txt
deactivate

# 关闭防火墙
systemctl stop firewalld.service

# 安装宝塔
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh