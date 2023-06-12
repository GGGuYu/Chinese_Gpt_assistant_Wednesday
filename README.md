# GPT中文语音助手(基于gpt镜像站,只是提供语音服务与一些GPT操作接口，语音服务使用阿里云语音合成与语音识别)

## 免责声明  ： 

请勿商用，使用时请尊重任何镜像站的版权，这里也不会提供任何gpt镜像站地址，请您在合法的情况下自行寻找。



## 环境安装：

仅支持Python3，暂不支持Python2

pip install setuptools

python -m pip install -r requirements.txt

python -m pip install .

还有一些必要的包暂时没有写在这里，后续补上，运行失败可根据提示补上缺失的包即可。

之后需要创建工具类中所需要的阿里云语音服务的相关ID与KEY，请使用您自己的，将它们配置在环境变量中，程序即可读取。

## 运行方式：

首先运行提供语音、记忆系统和相关操作接口的服务器，运行tests中的main.py即可，若运行失败，只需要根据错误安装上相关的包即可。
运行服务器成功后，将tests下的js文件夹下的main.js代码粘贴到您所要使用作为gpt入口的镜像站中，这里就不明确说明了,更改监控程序中相关的类选择器让程序可以监控到gpt回复并发出玩家回复即可。此时运行代码，连接成功，语音助手会提示你。

运行演示在:【G P T 读 原 神】 https://www.bilibili.com/video/BV1MM4y1e755/?share_source=copy_web&vd_source=e873459404f71c2ef697805a52452c7e

## 开发原因：

学生拙作，不喜勿喷。因为我的openaikey要过期了，所以我就想做个以平常可以用的镜像站为gpt入口的语音程序，欢迎二次开发。
