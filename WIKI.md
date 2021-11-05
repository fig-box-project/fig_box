### 状态码

```
201 成功创建资源
202 异步代码处理中,请稍后再次拉取
204 没有需要返回的数据
206 只成功了一部分
```

```
400 未知错误
401 未放token
402 未支付
403 权限不足,禁止
404 找不到页面
405 客户端的方法被禁止
406 无法接受
408 超时
409 发生了冲突,已存在
410 曾经有的资源现在没了
411 Length Required 属于客户端错误，表示由于缺少确定的 Content-Length 首部字段，服务器拒绝客户端的请求。
412错误，（Precondition failed），是HTTP协议状态码的一种，表示“未满足前提条件”。
422 传值不正确
423 资源被锁
501 目前未实现的API
```

### 启动命令

```
sudo uvicorn app.main:app --port 8000 --host 0.0.0.0 --reload
```

### Centos 系统的端口开启

```
systemctl stop firewalld.service    关闭防火墙
systemctl start firewalld.service   开启防火墙
systemctl staus firewalld.service   查看防火墙状态
firewall-cmd --zone=public --add-port=8080/tcp --permanent 开放指定端口
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload      重启防火墙
firewall-cmd --list-ports  查看开放了的端口
```

----------------------------------------------------------------
centOS配置一条龙

```
sudo passwd  # 设置密码
su root # 进入root
yum update
yum install screen
screen -S dev
yum install git
yum install python3.8
git clone https://github.com/normidar/my_fastapi
cd my_fastapi
python3 -m venv venv
source tutorial-env/bin/activate
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install -r requirements.txt

uvicorn app.main:app --port 8080 --host 0.0.0.0 --reload
uvicorn app.main:app --port 333 --host 0.0.0.0 --reload
uvicorn app.main:app --port 369 --host 0.0.0.0 --reload
```

----------------------------------------------------------------
> sudo python3 -m venv tutorial-env

> source tutorial-env/bin/activate

> yum install python3-devel
> pip3 install -r requirements.txt

> mkdir files

//安装screen请使用apt:
apt-get update apt-get install screen

screen -S name //创建 名为name的 screen screen -ls //列出所有screen screen -d -r [pid(名字前的数字)]  //进入screen tt

rm -rf files 强行删除文件夹 mkdir files 创建文件夹

> ctrl a d 退出screen
> exit 关闭screen窗口

# git 强制更新

sudo git fetch --all sudo git reset --hard origin/master

# 获取库的下载地址

https://github.com/normidar/my_fastapi/archive/master.zip

# 获取github中所有的tag

https://api.github.com/repos/normidar/my_fastapi/tags

> 检查包的信息<br>
pip3 show pyyaml



---------------

## 关于自动推送

```
del_db  
del_settings
pk_update
un_update
# 分别是删库,删设置,包更新,不更新代码
```