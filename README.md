### .下载代码
``` shell
$ git clone https://github.com/xmduhan/yyzj
```

### .同步Python环境
``` shell
$ cd yyzj
$ pipenv sync
```

### .讯飞Java sdk
``` shell
$ copy lfasr-client-sdk-x.x.x.xxxx-jar-with-dependencies.jar gateway/libs/
```

### .创建数据
``` shell
$ ./manage.py migrate
```

### .创建配置文件
``` shell
$ copy config.py.sample config.py
$ copy gateway/config.properties.sample gateway/config.properties
```

### .安装相关软件
``` shell
# for centos
$ sudo yum install unzip, tmux
# for ubuntu
$ sudo apt-get install unzip, tumx
```

### .启动守护进程
``` shell
# 启动守护进程前, 要记得先清空邮箱.
$ tmux
$ rename-session lfasr
$ ./lfasr.py
$ CTRL-b d

$ tmux
$ rename-session mail
$ ./mail.py
$ CTRL-b d
```

### .使用
```
# .编写邮件标题为"语音质检"
# .添加附件, 系统会自动识别附件中后缀为.wav的音频文件
# .可以将音频文件(*.wav)打包后上传, 压缩格式为zip
# .将邮件发送到接口地址
# .NOTE: 讯飞接口解析语音有时比较慢(数小时), 需要耐心等待
```
