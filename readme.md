## Python & R finance

金融后端指标画图

### API
基于flask的api后端，输入代码和日期，调用R绘图，python将金融指标图上传到CDN，返回CDN的URL链接


### RPC

基于python的json_rpc服务，获取金融数据，调用`tushare` python扩展，获取金融数据，参数与`tushare`一致，也可通过R的yahoo api获取，但是速度不如`tushare`快。