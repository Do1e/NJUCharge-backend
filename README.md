# 南大充电桩状态-后端

## 使用

运行`main.py`即可，将最新状态更新到`status.json`中。

* `utils/per_station.py`用于获取每个充电站点的插座ID，一般不会更新而且需要`token`验证所以在`main.py`中注释掉了。
* `utils/per_outlet.py`可获取每个插座的状态。

`sort_outlets.py`用于读取`status.json`并按照插座剩余时间排序。

查看实例HTML：
1. 在命令行启动一个http服务器：`python -m http.server 8000`
2. 访问`http://localhost:8000/example.html`
