import requests
import random
import re
from PIL import Image
from io import StringIO
import zipfile
import os
from io import BytesIO

err = ''

def getCaptchakey(data):
	cer = re.compile('\"key\":\s+\"([0-9a-z]*)\"',flags = 0)
	strlist = cer.findall(data)
	return strlist[0]

def getChanneluser(data):
	cer = re.compile('channeluser=([0-9]*)', flags = 0)
	strlist = cer.findall(data)
	if len(strlist) == 0:
		return '该手机号注册有问题，需要查看!'
	return strlist[0]

def getMccaNo(data,mccaName):
	cer = re.compile('mcca_no\":\s+(\d+),\s+\"mcca_name\":\s+\"' + mccaName, flags = 0)
	strlist = cer.findall(data)
	if len(strlist) == 0:
		global err 
		err = '已不存在<' + mccaName + '>服务，联系开发!'
		return 'error'
	return strlist[0]

def getMccNo(data,mccName):
	cer = re.compile('mcc_no\":\s+(\d+),\s+\"mcc_name\":\s+\"' + mccName, flags = 0)
	strlist = cer.findall(data)
	if len(strlist) == 0:
		global err 
		err = '已不存在<' + mccName + '>商品，联系开发!'
		return 'error'
	return strlist[0]

def getAreaNo(data,areaName):
	cer = re.compile(areaName + '\",\s+\"area_no\":\s+(\d+)', flags = 0)
	strlist = cer.findall(data)
	if len(strlist) == 0:
		global err 
		err = '已不存在<' + areaName + '>省份，联系开发!'
		return 'error'
	return strlist[0]

def getCityNo(data,cityName):
	cer = re.compile(cityName + '\",\s+\"city_no\":\s+(\d+)', flags = 0)
	strlist = cer.findall(data)
	if len(strlist) == 0:
		global err 
		err = '已不存在<' + cityName + '>城市，联系开发!'
		return 'error'
	return strlist[0]

def getBankNo(data,headbankName):
	cer = re.compile(headbankName + '\",\s+\"bank_no\":\s+(\d+)', flags = 0)
	strlist = cer.findall(data)
	if len(strlist) == 0:
		global err 
		err = '已不存在<' + headbankName + '>银行，联系开发!'
		return 'error'
	return strlist[0]

def getBrchbankNo(data,brchbankName):
	cer = re.compile(brchbankName + '\",\s+\"brchbank_no\":\s+\"(\d+)', flags = 0)
	strlist = cer.findall(data)
	if len(strlist) == 0:
		global err 
		err = '已不存在<' + brchbankName + '>支行，联系开发!'
		return 'error'
	return strlist[0]

def getPicPath(path, k):
	z = zipfile.ZipFile(path)
	cer = re.compile(k + '/照片/身份证正面\.')
	idcardfront = [filename for filename in z.namelist() if re.match(cer, filename)][0]
	cer = re.compile(k + '/照片/身份证反面\.')
	idcardback = [filename for filename in z.namelist() if re.match(cer, filename)][0]
	cer = re.compile(k + '/照片/店铺内景\.')
	goodsphoto = [filename for filename in z.namelist() if re.match(cer, filename)][0]
	cer = re.compile(k + '/照片/店铺外景\.')
	shopphoto = [filename for filename in z.namelist() if re.match(cer, filename)][0]
	cer = re.compile(k + '/照片/业务员与申请人在收银台合影\.')
	groupphoto = [filename for filename in z.namelist() if re.match(cer, filename)][0]
	cer = re.compile(k + '/照片/银行卡正面\.')
	authbankcardfront = [filename for filename in z.namelist() if re.match(cer, filename)][0]
	cer = re.compile(k + '/照片/银行卡反面\.')
	authbankcardback = [filename for filename in z.namelist() if re.match(cer, filename)][0]
	cer = re.compile(k + '/照片/营业执照\.')
	licensephotolist = [filename for filename in z.namelist() if re.match(cer, filename)]
	if len(licensephotolist) != 0:
		licensephoto = licensephotolist[0]
		piclist = [idcardfront, idcardback, goodsphoto, shopphoto, groupphoto, authbankcardfront, authbankcardback, licensephoto]
	else:
		piclist = [idcardfront, idcardback, goodsphoto, shopphoto, groupphoto, authbankcardfront, authbankcardback]
	#解压照片
	print('------>  正在解压zip中的图片。。。')
	with open('idcardfront.' + piclist[0].split('.')[1], 'wb') as f:
		f.write(z.read(piclist[0]))
	with open('idcardback.' + piclist[1].split('.')[1], 'wb') as f:
		f.write(z.read(piclist[1]))
	with open('goodsphoto.' + piclist[2].split('.')[1], 'wb') as f:
		f.write(z.read(piclist[2]))
	with open('shopphoto.' + piclist[3].split('.')[1], 'wb') as f:
		f.write(z.read(piclist[3]))
	with open('groupphoto.' + piclist[4].split('.')[1], 'wb') as f:
		f.write(z.read(piclist[4]))
	with open('authbankcardfront.' + piclist[5].split('.')[1], 'wb') as f:
		f.write(z.read(piclist[5]))
	with open('authbankcardback.' + piclist[6].split('.')[1], 'wb') as f:
		f.write(z.read(piclist[6]))
	if len(licensephotolist) != 0:
		with open('licensephoto.' + piclist[7].split('.')[1], 'wb') as f:
			f.write(z.read(piclist[7]))
	return piclist

def getUserNames(path):
	cer = re.compile('.+：(.*)\r\n',flags = 0)
	z = zipfile.ZipFile(path)
	s = set()
	for filename in z.namelist():
		name = filename.split('/')[0]
		s.add(name)
	#return s
	diction = {}
	for name in s:
		#print(name)
		file_bytes = z.read(name + '/' + name + '.txt')
		content = str(file_bytes, encoding = "utf-8")
		strlist = cer.findall(content)
		pertradeamount = 1
		if '500以下' == strlist[11]:
			pertradeamount = 1
		elif '500-1,000' == strlist[11]:
			pertradeamount = 500
		elif '1,001-5,000' == strlist[11]:
			pertradeamount = 1001
		elif '5,001-10,000' == strlist[11]:
			pertradeamount = 5001
		elif '10,000以上' == strlist[11]:
			pertradeamount = 10000
		
		monthtradeamount = 1
		if '0-100,000' == strlist[12]:
			monthtradeamount = 1
		elif '10,001-50,000' == strlist[12]:
			monthtradeamount = 10001
		elif '50,001-100,000' == strlist[12]:
			monthtradeamount = 50001
		elif '100,000以上' == strlist[12]:
			monthtradeamount = 100000
		
		params = {
			'personname':strlist[0],
			'idnumber':strlist[1],
			'email':strlist[2],
			'mobile':strlist[3],
			'areaName':strlist[4],
			#'province':
			'cityName':strlist[5],
			#'city':
			'addr':strlist[6],
			'telephone':strlist[7],
			'nickname':strlist[8],
			'mccaName':strlist[9],
			'mccName':strlist[10],
			#'mcc':
			'terminalcount':1,
			'pertradeamount':pertradeamount,
			'monthtradeamount':monthtradeamount,
			'headbankName':strlist[13],
			#'headbankname':
			'banknamedefault':-1,
			'old_addr':'new',
			'bankname':strlist[14],
			#'brchbank_code':
			'banktype':1,
			'bankuser':strlist[15],
			'bankaccount':strlist[16],
			'confirmbankaccount':strlist[16]
		}
		diction[name] = params
	return diction

#根据本地zip包获取数据
path = input('请输入zip包全路径(如：d:/商户申请记录20160926-162227.zip)：\n')

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	'Connection': 'keep-alive',
	'Host': 'qfpay.com',
	'X-Requested-With': 'XMLHttpRequest'
}

#需要检测的用户
checklilst = []

#随机数
randomt = str(random.random())

basicUrl = 'https://qfpay.com/qudao/'

param = {
	't':randomt
}

s = requests.Session()

#ssl
#r = s.get(basicUrl + 'getcaptcha',params=param,verify=False)
r = s.get(basicUrl + 'getcaptcha',params=param)

#登录参数之一captchakey
captchakey = getCaptchakey(r.text)

#获取验证码
r = s.get(basicUrl + 'captcha/image/' + captchakey + '/')
# with open('code.png','wb') as f:
# 	f.write(r.content)

# i = Image.open('code.png')
# i.show()
i = Image.open(BytesIO(r.content))
i.show()


captcha = input('\n请输入验证码：')

#登录参数
postDict = {
	'username':'用户名',
	'password':'密码',
	'captcha':captcha,
	'captchakey':captchakey
}

print('\n开始登录。。。')
r = s.post(basicUrl + 'channel_login',data=postDict,headers = headers)
print('\n登录成功！！！\n')

#获取服务数据
print('获取申请服务信息。。。\n')
r = s.get('https://qfpay.com/util/mcca/')
mccaStr = (r.content).decode('unicode-escape')

#获取省份数据
print('获取申请省份信息。。。\n')
r = s.get('https://qfpay.com/util/area/')
areaStr = (r.content).decode('unicode-escape')

#获取开户银行数据
print('获取申请银行信息。。。\n')
r = s.get('https://qfpay.com/util/bank/')
bankStr = (r.content).decode('unicode-escape')

print('解析zip数据。。。\n')
dic = getUserNames(path)

num = 1
count = len(dic)

for k in dic:
	mobile = dic[k]['mobile']
	print('正在处理第< ' + str(num)  + ' / ' + str(count) + ' >个用户(' + mobile + ')申请。。。')
	mccaName = dic[k]['mccaName']
	mccName = dic[k]['mccName']
	areaName = dic[k]['areaName']
	cityName = dic[k]['cityName']
	headbankName = dic[k]['headbankName']
	brchbankName = dic[k]['bankname']

	#根据服务名获取服务no
	mcca_no = getMccaNo(mccaStr, mccaName)
	if 'error' == mcca_no:
		print('------>  ' + err + '跳过该用户申请\n')
		err = err + mobile
		num = num +1
		continue

	#获取商品no
	r = s.get('https://qfpay.com/util/mcc/' + mcca_no + '/')
	mcc_no = getMccNo((r.content).decode('unicode-escape'), mccName)
	if 'error' == mcc_no:
		print('------>  ' + err + '跳过该用户申请\n')
		err = err + mobile
		num = num +1
		continue

	#根据省份名获取省份no
	area_no = getAreaNo(areaStr, areaName)
	if 'error' == area_no:
		print('------>  ' + err + '跳过该用户申请\n')
		err = err + mobile
		num = num +1
		continue

	#获取城市no
	r = s.get('https://qfpay.com/util/city/' + area_no + '/')
	city_no = getCityNo((r.content).decode('unicode-escape'), cityName)
	if 'error' == city_no:
		print('------>  ' + err + '跳过该用户申请\n')
		err = err + mobile
		num = num +1
		continue

	#根据开户银行名获取开户银行no
	bank_no = getBankNo(bankStr, headbankName)
	if 'error' == bank_no:
		print('------>  ' + err + '跳过该用户申请\n')
		err = err + mobile
		num = num +1
		continue

	#获取开户行网点no
	r = s.get('https://qfpay.com/util/brchbank/' + bank_no + '_' + city_no + '/')
	brchbank_no = getBrchbankNo((r.content).decode('unicode-escape'), brchbankName)
	if 'error' == brchbank_no:
		print('------>  ' + err + '跳过该用户申请\n')
		err = err + mobile
		num = num +1
		continue

	#组装请求参数，pop掉无用参数
	postDict = dic[k]
	postDict['province'] = area_no
	postDict['city'] = city_no
	postDict['mcc'] = mcc_no
	postDict['headbankname'] = bank_no
	postDict['brchbank_code'] = brchbank_no
	postDict.pop('areaName')
	postDict.pop('cityName')
	postDict.pop('mccaName')
	postDict.pop('mccName')

	piclist = getPicPath(path, k)
	
	z = zipfile.ZipFile(path)

	postDict3 = {
		'idcardfront':'',
		'idcardback':'',
		'goodsphoto':'',
		'shopphoto':'',
		'groupphoto':'',
		'licensephoto':'',
		'rentalagreement':'',
		'invoicephoto':'',
		'purchaselist':'',
		'authbankcardfront':'',
		'authbankcardback':'',
		'otherphoto':'',
	}

	#file_bytes = z.read(piclist[0])

	multiple_files = [
		{'idcardfront': ('idcardfront.' + piclist[0].split('.')[1], open('idcardfront.' + piclist[0].split('.')[1], 'rb'), 'multipart/form-data')},
		{'idcardback': ('idcardback.' + piclist[1].split('.')[1], open('idcardback.' + piclist[1].split('.')[1], 'rb'), 'multipart/form-data')},
		{'goodsphoto': ('goodsphoto.' + piclist[2].split('.')[1], open('goodsphoto.' + piclist[2].split('.')[1], 'rb'), 'multipart/form-data')},
		{'shopphoto': ('shopphoto.' + piclist[3].split('.')[1], open('shopphoto.' + piclist[3].split('.')[1], 'rb'), 'multipart/form-data')},
		{'groupphoto': ('groupphoto.' + piclist[4].split('.')[1], open('groupphoto.' + piclist[4].split('.')[1], 'rb'), 'multipart/form-data')},
		{'authbankcardfront': ('authbankcardfront.' + piclist[5].split('.')[1], open('authbankcardfront.' + piclist[5].split('.')[1], 'rb'), 'multipart/form-data')},
		{'authbankcardback': ('authbankcardback.' + piclist[6].split('.')[1], open('authbankcardback.' + piclist[6].split('.')[1], 'rb'), 'multipart/form-data')}
	]
	if len(piclist) == 8:
		multiple_files.append({'licensephoto': ('licensephoto.' + piclist[7].split('.')[1], open('licensephoto.' + piclist[7].split('.')[1], 'rb'), 'multipart/form-data')})

	print('------>  查看该用户是否为审核失败用户。。。')
	param = {
		'startTime':'',
		'endTime':'',
		'query':mobile
	}
	r = s.post(basicUrl + 'apply/list/8', params = param)
	cer = re.compile('.*(无数据).*')
	strlist = cer.findall(r.text)
	if len(strlist) == 0:
		print('------>  ' + mobile + ' 用户为审核失败用户,执行修改')
		cer2 = re.compile('(/qudao/edit_fulfill/\d+)')
		strlist = cer2.findall(r.text)
		if len(strlist) != 0:
			print('------>  提交基本信息表单。。。')
			s.post('https://qfpay.com' + strlist[0], data = postDict)
			for i in range(7):
				print('      ------>  上传照片<' + str(i+1) + '/7>')
				s.post('https://qfpay.com/upgrade/upload/channel/' + strlist[0][20:],files=multiple_files[i])
			s.post(basicUrl + 'confirm_submit/' + strlist[0][20:],data=postDict3)
	else:	
		postDict2 = {
			'user_type':'4',
			'mobile':mobile
		}
		print('------>  提交手机号。。。')
		r = s.post(basicUrl + 'apply/basic',data=postDict2,headers = headers, allow_redirects=False)

		channeluser = getChanneluser(str(r.headers))
		if channeluser == '该手机号注册有问题，需要查看!':
			print("------>  " + channeluser + ',跳过<' + mobile + '>该用户！\n')
			num = num + 1
			checklilst.append(mobile)
			continue
		
		print('------>  提交基本信息表单。。。')
		s.post(basicUrl + 'apply/profile?channeluser=' + channeluser,data=postDict,headers = headers)

		headers['Referer']='https://qfpay.com/qudao/apply/voucher?channeluser=' + channeluser
		
		print('------>  上传照片。。。')
		for i in range(len(multiple_files)):
			print('      ------>  上传照片<' + str(i+1) + '/' + str(len(multiple_files)) + '>')
			s.post('https://qfpay.com/upgrade/upload/channel/' + channeluser,files=multiple_files[i],headers=headers)

		s.post(basicUrl + 'apply/voucher?channeluser=' + channeluser,headers=headers,data=postDict3)
		#print('申请完成< ' + str(num) + ' / ' + str(count) + '> ')
	print('------>  申请完成(' + str(num) + ' / ' + str(count) + ')\n')
	num = num + 1
	#删除图片
	# os.remove('idcardfront.' + piclist[0].split('.')[1])
	# os.remove('idcardback.' + piclist[1].split('.')[1])
	# os.remove('goodsphoto.' + piclist[1].split('.')[1])
	# os.remove('shopphoto.' + piclist[3].split('.')[1])
	# os.remove('groupphoto.' + piclist[4].split('.')[1])
	# os.remove('authbankcardfront.' + piclist[5].split('.')[1])
	# os.remove('authbankcardback.' + piclist[6].split('.')[1])
	# os.remove('code.png')

print('============ 完成所有用户申请！============\n')

if len(checklilst) != 0:
	print('以下用户需要手动查看：')
	for u in checklilst:
		print(u)
	print('')
if err != '':
	print(err + '\n')
input('按回车键退出：')