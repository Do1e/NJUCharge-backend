# 南大充电桩状态-后端

## 使用

运行`main.py`即可，将最新状态更新到`status.json`中。

* `utils/per_station.py`用于获取每个充电站点的插座ID，一般不会更新而且需要`token`验证所以在`main.py`中注释掉了。
* `utils/per_outlet.py`可获取每个插座的状态。
