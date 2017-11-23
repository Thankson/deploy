##### <a href="#1安装环境">安装环境</a>
##### <a href="#2安装准备">安装准备</a>
##### <a href="#3安装步骤">安装步骤</a>
##### <a href="#4Redis启动停止测试">Redis启动停止测试</a>
##### <a href="#5打开防火墙规则">打开防火墙规则</a>

## <a name="1安装环境">安装环境</a>:
###### 操作系统：Centos 6.5 -64bit
###### 安装路径：/usr/local/redis

## <a name="2安装准备">安装准备</a>:
###### 准备redis安装包 redis-4.0.2.tar.gz，并放在/usr/local/src/redis-4.0.2.tar.gz目录下（redis-4.0.2.tar.gz为最新稳定版stable ，截至2017/11/17）

## <a name="3安装步骤">安装步骤</a>:
1. 创建目录 /usr/local/redis
* 编译安装
    * 进入cd /usr/local/src/
    * 解压redis-4.0.2.tar.gz ， tar -zxvf redis-4.0.2.tar.gz && cd redis-4.0.2
    * make
    * make PREFIX=/usr/local/redis install
* Redis配置    
###### vim /usr/local/redis/etc/redis.conf
```
# 修改一下配置
daemonize yes
timeout 300
loglevel verbose
logfile stdout
```
* redis环境变量配置
###### vim /etc/profile
```
export PATH="$PATH:/usr/local/redis/bin"
source /etc/profile
```
* Redis 启动脚本
###### 添加Redis 启动脚本

## <a name="4Redis启动停止测试">Redis启动停止测试</a>:
```
service redis start   #或者 /etc/init.d/redis start  
service redis stop   #或者 /etc/init.d/redis stop

# 查看redis进程
ps -el|grep redis

# 端口查看
netstat -an|grep 3306
```

## <a name="5打开防火墙规则">打开防火墙规则</a>:
###### vim /etc/sysconfig/iptables
```
# 增加内容
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 6379 -j ACCEPT

# 重启火墙规则立即生效
service iptables restart
```
