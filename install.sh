# yes | source /install.sh
# git config --global credential.helper store

# check system
if [[ $(uname) == 'Darwin' ]]; then
    echo "Mac OS"
fi


if [[ $(uname) == 'Linux' ]]; then
    source /etc/os-release
    echo "$ID"
    case $ID in
    debian|ubuntu|devuan|raspbian)
        echo "apt-get"
#        sudo apt-get install lsb-release
        ;;
    centos|fedora|rhel)
        pgkey="yum"
        echo "$pgkey"
        installGitProject $pgkey
#        if test "$(echo "$VERSION_ID >= 22" | bc)" -ne 0; then
#            yumdnf="dnf"
#        fi
#        sudo $yumdnf install -y redhat-lsb-core
        ;;
    *)
        exit 1
        ;;
    esac
fi

installGitProject(){
  $1 -y install git
  git clone https://github.com/normidar/fig_box
}

#yum install -y git
#yum install -y python3.8
## yum update
## 安装screen并安装dev
#yum install -y epel-release
#yum install -y screen
## screen -S dev
#cd /
#mkdir my_dev
#cd /my_dev
#git clone https://github.com/normidar/my_fastapi
#cd my_fastapi
#python3.8 -m venv tutorial-env
#source tutorial-env/bin/activate
#pip3.8 install --upgrade pip
#pip3.8 install --upgrade setuptools
#pip3.8 install -r requirements.txt
#deactivate
#
## 安装puller
#cd /
#mkdir pull
#cd /pull
#git clone https://github.com/normidar/my_fastapi
#cd my_fastapi
#python3.8 -m venv tutorial-env
#source tutorial-env/bin/activate
#pip3.8 install --upgrade pip
#pip3.8 install --upgrade setuptools
#pip3.8 install -r requirements.txt
#deactivate
#
## 安装oil
#cd /
#mkdir oil
#cd /oil
#git clone https://github.com/normidar/my_fastapi
#cd my_fastapi
#python3.8 -m venv tutorial-env
#source tutorial-env/bin/activate
#pip3.8 install --upgrade pip
#pip3.8 install --upgrade setuptools
#pip3.8 install -r requirements.txt
#deactivate
#
## 关闭防火墙
#systemctl stop firewalld.service
#
## 设置为密码记住的功能
#git config --global credential.helper store
#
## 克隆Blog的文件
#cd /
#mkdir www
#cd www
#mkdir wwwroot
#cd wwwroot
#mkdir datasview.com
#cd datasview.com
#git clone https://github.com/applelizihao/Blog
#
#
## 安装宝塔
#yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh
#
## source tutorial-env/bin/activate
## uvicorn app.main:app --port 8080 --host 0.0.0.0 --reload
## uvicorn app.main:app --port 333 --host 0.0.0.0 --reload
## uvicorn app.main:app --port 369 --host 0.0.0.0 --reload
## uvicorn app.main:app --port 4444 --host 0.0.0.0 --reload