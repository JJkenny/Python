import requests
import time
# 下载器的类
class downloader:
	# 构造函数
	def __init__(self):
		self.url = 'http://mirror2.internetdownloadmanager.com/idman627build5.exe?b=1&filename=idman627build5.exe'
		# 要开的线程数
		self.num = 8
		# 存储文件的名字，从url最后面开始取
		self.name = self.url.split('/')[-1]
		# head方法去请求url
		r = requests.head(self.url)
		# headers中取出数据的长度
		self.total = int(r.headers['Content-Length'])
		print('total is %s' % (self.total))

	def get_range(self):
		ranges = []
		# 比如total是50，线程数是4个。offset就是12
		offset = int(self.total/self.num)
		for i in range(self.num):
			if i == self.num-1:
				#最后一个线程，不指定结束为止，取到最后
				ranges.append((i*offset, ''))
			else:
				#每个线程取得区间
				ranges.append((i*offset, (i+1)*offset))
		# range大概是[(0,12),(12,24),(25,36),(36,'')]
		return ranges
	
	def run(self):
		with open('a.exe', 'wb') as f:
			for ran in self.get_range():
				# 拼出Range参数 获取分片数据
				r = requests.get(self.url, headers={'Range':'Bytes=%s-%s' % ran,'Accept_Encoding':'*'})
				# seek到相应位置
				f.seek(ran[0])
				# 写数据
				f.write(r.content)

if __name__=='__main__':
	st = time.time()
	down = downloader()
	down.run()
	ed = time.time()
	print('time is %0.2f' % (ed - st))