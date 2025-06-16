# 南大充电桩状态-后端

## 使用

运行`main.py`即可，将最新状态更新到`output/status.json`中，或者也可通过`--campus`指定校区，目前仅支持鼓楼和仙林。


* `utils/per_station.py`用于获取每个充电站点的插座ID。
* `utils/per_outlet.py`可获取每个插座的状态。

`sort_outlets.py`用于读取`status.json`并按照插座剩余时间排序，或者也可通过`--campus`指定校区。

查看实例HTML：
1. 在命令行启动一个http服务器：`python -m http.server 8000`
2. 访问`http://localhost:8000/example1.html` 或 `http://localhost:8000/example2.html`
