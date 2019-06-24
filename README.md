# flatfish
supervisor ui with django

# 功能
- supervisor 多主机管理UI
- 弹窗显示supervisor log
- 前端添加supervisor node
- 用户认证
- 权限管理
- 移动端

# 截图
![登录](https://raw.githubusercontent.com/shijieqin/PicBed/master/20190624101431.png)
![HOME](https://raw.githubusercontent.com/shijieqin/PicBed/master/20190624101613.png)
![添加节点](https://raw.githubusercontent.com/shijieqin/PicBed/master/20190624101911.png)
![功能页面](https://raw.githubusercontent.com/shijieqin/PicBed/master/20190624102007.png)
![项目页面](https://raw.githubusercontent.com/shijieqin/PicBed/master/20190624102100.png)
![日志页面](https://raw.githubusercontent.com/shijieqin/PicBed/master/20190624102150.png)
![admin页面](https://raw.githubusercontent.com/shijieqin/PicBed/master/20190624102504.png)
![新增权限](https://raw.githubusercontent.com/shijieqin/PicBed/master/20190624125524.png)

# 安装
```
1、克隆代码到本地
2、执行python manage.py migrate来初始化数据库
3、执行python manage.py createsuperuser创建管理员用户
4、执行python manage.py runserver 启动
5、访问http://127.0.0.1/supervisor/node
```
# 说明
- 管理界面(/admin/)
    - 用户管理
    - 权限管理
    - 节点删除
- 进程管理访问(/supervisor/node/)
    - node管理界面
    - 模块管理界面
    - 项目管理界面
- 子进程名必须是 env-project-num 格式，如: testENV-pr-2。
- 执行python manage.py runserver 0.0.0.0:18000 的方式来修改监听ip和端口
- 连接按钮暂时没有实现相应功能，页面刷新时会自动连接。节点显示Connected，说明已经连接.


- 项目是初版，一直没有时间去更新，许多页面没有做跳转，会报404，此次应[@potoo0](https://github.com/potoo0)的需求，更新README，
加入详细的使用说明。感谢[@potoo0](https://github.com/potoo0)提出的意见