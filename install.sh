# yes | source /install.sh
# git config --global credential.helper store

# methods
updatePg(){
  echo "to be update packages"
  $1 -y update 1>log.txt
}
installGitProject(){
  echo "to be install git"
  $1 -y install git 1>log.txt
  case "$(git clone https://github.com/normidar/fig_box 1>log.txt)" in
    "fatal:"*)
      echo "fig_box is existing"
      ;;
    *)
      echo "install succeed"
      ;;
  esac
}
installPython(){
  case "$(python3 --version 2>&1)" in
    *" 3.6"*)
        echo "do not need to install python3"
        return 6
        ;;
    *" 3.7"*)
        echo "do not need to install python3"
        return 7
        ;;
    *" 3.8"*)
        echo "do not need to install python3"
        return 8
        ;;
    *" 3.9"*)
        echo "do not need to install python3"
        return 9
        ;;
    *)
        echo "python3 install start"
        $1 -y install python3.8
        return 8
        ;;
  esac
}
installScreen() {
  if [[ $(1) == 'yum' ]]; then
    yum -y install epel-release &>log.txt
  fi
  $1 -y install screen
  echo "screen installed"
}
createEvnAndInstall(){
  python3
}

# package tool string
pgkey="null"

# check system
if [[ $(uname) == 'Darwin' ]]; then
    echo "Mac OS"
fi


if [[ $(uname) == 'Linux' ]]; then
    source /etc/os-release
    echo "$ID"
    case $ID in
    debian|ubuntu|devuan|raspbian)
        pgkey="apt-get"

#        sudo apt-get install lsb-release
        ;;
    centos|fedora|rhel)
        pgkey="yum"

#        if test "$(echo "$VERSION_ID >= 22" | bc)" -ne 0; then
#            yumdnf="dnf"
#        fi
#        sudo $yumdnf install -y redhat-lsb-core
        ;;
    *)
        echo "can't find system type'"
        exit 1
        ;;
    esac
fi

echo $pgkey
updatePg $pgkey
installGitProject $pgkey
installPython $pgkey
num=$?
pythonNum="python3."${num}
pipNum="pip3."${num}
echo "$pythonNum"
echo "$pipNum"
installScreen $pgkey
# into the git folder
cd fig_box || exit
$pgkey -y install python3.8-venv
$pythonNum -m venv tutorial-env
source tutorial-env/bin/activate
$pipNum install --upgrade pip
$pipNum install --upgrade setuptools
$pipNum install -r requirements.txt
screen_name="fig_box"
screen -dmS $screen_name
cmd="python3 main.py";
screen -x -S $screen_name -p 0 -X stuff "$cmd"
screen -x -S $screen_name -p 0 -X stuff '\n'

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
# apt install python3.8-venv
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