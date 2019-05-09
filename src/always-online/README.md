# Always-online

这个小工具能让你保持移动校园网络的在线状态，被下线后能自动恢复（仅适用于中南大学）。在 macOS 上顺利运行，其他系统可能需要稍加修改，欢迎提交 Pull Request。

## 用法
1. 安装 pipenv：`pip install pipenv`
1. 安装依赖：`pipenv sync && pipenv shell`
1. 复制 `credentials_example.py` 为 `credentials.py` 并修改账号密码
1. 运行：`python always-online.py`