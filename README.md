##### 作业要求

```
1. 用户加密认证
2. 多用户同时登陆
3. 每个用户有自己的家目录且只能访问自己的家目录
4. 对用户进行磁盘配额、不同用户配额可不同
5. 用户可以登陆server后，可切换目录
6. 查看当前目录下文件
7. 上传下载文件，保证文件一致性
8. 传输过程中现实进度条
9.支持断点续传
```

##### 程序的功能实现

```
1、多用户同时登录注册（已有用户：xiaoyu / 123456）
2、上传/下载文件（已有示例文件）
3、查看不同用户自己家得目录下文件，且只能访问自己的家目录
4、对用户进行磁盘配额，不同用户配额不同（使用random函数，随机给用户一个内存大小（10m-20m））
5、用户登录后，可对用户目录下文件目录进行操作，包含：ls、cd 命令
6、上传下载文件，保证文件一致性，且在传输过程中实现进度条
7、分别实现client 和 server 端操作的记录日志
```


##### 脚本文件介绍

```
D:.
│  __init__.py
│
├─FTPClient                  # FTPclient端的目录
│  │  ftp_client.py          # ftp clent 脚本文件
│  │
│  └─SampleFolder            # 客户端文件存放目录
│          alt_demo-openrc.sh
│          id_rsa
│          id_rsa.pub
│          id_rsa1111
│          ofile
│
└─FTPServer                  # FTPServer端目录
    │  __init__.py
    │
    ├─bin
    │      ftp_server.py     # ftp server 脚本启动文件
    │      __init__.py
    │
    ├─conf
    │  │  settings.py        # 目录配置文件脚本
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          settings.cpython-36.pyc
    │          __init__.cpython-36.pyc
    │
    ├─db                    # 用户登记目录
    │      xiaoyu
    │      xiess
    │
    ├─home                  # 用户文件存储目录
    │  ├─xiaoyu
    │  │  │  demo-openrc.sh
    │  │  │  ofile
    │  │  │
    │  │  └─others
    │  └─xiess
    │      │  ofile
    │      │
    │      └─others
    ├─logs
    │      client_sys.log   # 客户端操作日志
    │      server_sys.log   # 服务端操作日志
    │
    └─src
        │  common.py        # 日志生成脚本
        │  user.py          # 用户类及方法
        │
        ├─__init__.py
        └─__pycache__
                common.cpython-36.pyc
                user.cpython-36.pyc
```

##### 程序使用示例
用户登陆界面

```
|------User Login Interface------
    1: Land
    2: Register
    3: Sign out
    
|--Input Your Choice>>>:
```
登陆操作

```
|--Input Your Choice>>>:1
|--Input Your Username>>>:xiaoyu
|--Input Your Password>>>:123456
|--Login Success....
------Operation instruction------
    1: Uploading files
    2: Download the file
    3: View the files under the directory
    4: Switch directory operation
    5、Sign out
    
|--Input Your Choice Operate>>>:
```

退出操作

```
------Operation instruction------
    1: Uploading files
    2: Download the file
    3: View the files under the directory
    4: Switch directory operation
    5、Sign out
    
|--Input Your Choice Operate>>>:5
|------User Login Interface------
    1: Land
    2: Register
    3: Sign out
    
|--Input Your Choice>>>:3
```
