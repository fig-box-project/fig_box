
状态码
201 成功创建资源
202 异步代码处理中,请稍后再次拉取
204 没有需要返回的数据
206 只成功了一部分

400 未知错误
401 未放token
402 未支付
403 权限不足,禁止
404 找不到页面
405 客户端的方法被禁止
406 无法接受
408 超时
409 发生了冲突
410 曾经有的资源现在没了
422 传值不正确
423 资源被锁
501 目前未实现的API


sudo uvicorn app.main:app --port 5000 --host 0.0.0.0 --reload


----------------------------------------------------------------


>sudo python3 -m venv tutorial-env 

>source tutorial-env/bin/activate 

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
