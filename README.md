
> 状态码
201 成功创建资源
202 异步代码处理中,请稍后再次拉取
204 没有需要返回的数据
206 只成功了一部分

> 400 未知错误
401 未放token
402 未支付
403 权限不足,禁止
404 找不到页面
405 客户端的方法被禁止
406 无法接受
408 超时
409 发生了冲突,已存在
410 曾经有的资源现在没了
422 传值不正确
423 资源被锁
501 目前未实现的API


sudo uvicorn app.main:app --port 8000 --host 0.0.0.0 --reload

Centos 系统的端口开启
systemctl stop firewalld.service    关闭防火墙
systemctl start firewalld.service   开启防火墙
systemctl staus firewalld.service   查看防火墙状态
firewall-cmd --zone=public --add-port=8080/tcp --permanent 开放指定端口
firewall-cmd --reload      重启防火墙
firewall-cmd --list-ports  查看开放了的端口
----------------------------------------------------------------


>sudo python3 -m venv tutorial-env 

>source tutorial-env/bin/activate 

>yum install python3-devel
>pip3 install -r requirements.txt 

>mkdir files

<!-- source venv/bin/activate -->

//安装screen请使用apt:
apt-get update
apt-get install screen

screen -S name  //创建 名为name的 screen
screen -ls  //列出所有screen
screen -d -r [pid(名字前的数字)]  //进入screen tt

rm -rf files 强行删除文件夹
mkdir files 创建文件夹

> ctrl a d 退出screen
> exit 关闭screen窗口

# git 强制更新
sudo git fetch --all
sudo git reset --hard origin/master

# 获取github中所有的tag
https://api.github.com/repos/normidar/my_fastapi/tags
