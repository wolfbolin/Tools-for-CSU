# Keep-online

*Forked from [fr0der1c/always-online](https://github.com/fr0der1c/always-online)*

这个小工具能自动监测网络状态，并在掉线后能自动重连。（仅适用于中南大学中国移动网络）

此版本针对于 Linux 平台编写，并且需要用户自行设计计时器反复调用，已针对Python2与Python3进行优化。

**多平台**

Linux：<https://github.com/wolfbolin/csu-keep-online>

MacOS：<https://github.com/fr0der1c/always-online>



## 环境部署

基本目的在于安装`requests`包，其他实现方式也是可以的。

### virtualenv

1. 安装**virtualenv**：`pip install virtualenv`
1. 创建虚拟环境：`virtualenv venv`
1. 进入虚拟环境：`source venv/bin/activate`
1. 安装依赖包：`pip install -r requirements.txt`或`pip install requests`
1. 退出虚拟环境：`deactivate`

### Pipenv

Pipfile与Pipfile.lock只针对Python3.7编写，如有需要自行修改版本。

1. 安装 pipenv：`pip install pipenv`
2. 安装依赖：`pipenv sync && pipenv shell`或`pipenv update`
3. 运行：`python keep-online-pyK.py`



## 运行程序

请在配置文件中填充您的帐号密码

1. 复制 `config_example.py` 为 `config.py` 并修改账号密码

请根据虚拟环境中的Python调整运行的代码版本

1. 在虚拟环境中运行程序：`python keep-online-pyK.py`
2. 在全局运行程序：`venv/bin/python keep-online-pyK.py`



## 修改日志

相比于*fr0der1c/always-online*的版本

1. 移除调用Chrome内核相关代码
2. 修改判断在线状态代码逻辑
3. 修改登录帐号代码逻辑
4. 删除了一些骚话
5. 删除了定时器功能（可使用crontab代替）
6. 基本上等于重写了



**Email：me@wolfbolin.com**