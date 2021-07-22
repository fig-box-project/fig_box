# Figboxのインストール

## 前準備

システムに必要なものは以下：

- git(プロジェクトをダンロード)
- python3.6以上
- screen(バックグラウンドでプロジェクトを実行)

これらのダンロード方法：

centOS:

```shell
su root
yum update
yum install screen
yum install git
yum install python3.8
```

Debian、Ubuntu:

```shell
sudo su
apt-get update
apt-get install screen
apt-get install git
apt-get install python3.8
```

## Figboxインストール手順:

```shell
cd /
git clone https://github.com/normidar/fig_box
cd fig_box
screen -S dev
python3 -m venv tutorial-env
source tutorial-env/bin/activate
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install -r requirements.txt
python3 main.py
```

> これでサービスは起動します。




