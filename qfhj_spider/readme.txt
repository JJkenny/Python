钱方好近商户申请以及结果查看爬虫

我司和钱方好近合作，我们作为中间商，客户提交申请资料给我们，然后我们统一把客户的申请资料手动录入到钱方好近的系统中，
这个工作量很大，而且容易出错，他们的系统有炒鸡慢，所以我就写了两个爬虫。

pyqfhj_sign_in.py
这个是商户申请爬虫，从我们后台下载客户资料（一个zip包，里面是申请用户的资料和照片）。

pyqfhj_result.py
这个事结果查询爬虫，自动从我们后台查询出已申请待审核的用户，然后自动到钱方的系统中查询他们的结果，把所有结果统计到一个表格中自动导入我们的系统中。

