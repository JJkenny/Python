import re
import requests
import random
from PIL import Image
import os
import xlwt
import time

def getCaptchakey(data):
	cer = re.compile('\"key\":\s+\"([0-9a-z]*)\"',flags = 0)
	strlist = cer.findall(data)
	return strlist[0]

s = requests.Session()

host = 'http://120.55.137.181:5102/'
#host = 'http://localhost:8080/'

headers = {
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	'Connection': 'keep-alive',
	'X-Requested-With': 'XMLHttpRequest',
	'Content-Type': 'application/json; charset=UTF-8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8'
}

postData = '{"username":"用户名","password":"密码"}'

print('开始登录钱包后台。。。\n')
s.post(host + 'yfpay_admin/user/login', data = postData, headers = headers)
print('登录成功！！！\n')

postData = {
	'bean':'preMerchantapply',
	'method':'page',
	'STATUS':'APPLYED_WAIT_VERIFY',
	'page':'1',
	'rows':'300'
}

print('获取商户申请记录。。。\n')
r = s.post(host + 'yfpay_admin/process', data = postData)
users = []

for row in r.json()['rows']:
	user = {}
	user['mobile'] = row['MOBILE']
	user['custcode'] = row['CUST_CODE']
	users.append(user)

print('===== 成功获取了<' + str(len(users)) + '>个已申请待审核用户 =====')

#登录钱方好近begin
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
i = Image.open(BytesIO(r.content))
i.show()

print('\n开始登录钱方好近。。。')
captcha = input('\n请输入验证码：')

#登录参数
postDict = {
	'username':'用户名',
	'password':'密码',
	'captcha':captcha,
	'captchakey':captchakey
}

r = s.post(basicUrl + 'channel_login',data=postDict,headers = headers)
print('\n登录成功！！！\n')
#登录钱方好近end

#审核通过
successlist = []
#审核拒绝
refuselist = []
#审核失败
faillist = []
#三个都没找到的
checklist = []

cer = re.compile('.*(无数据).*');

#处理审核通过的用户
length = str(len(users))
for i,user in enumerate(users):
	param = {
		'startTime':'',
		'endTime':'',
		'query':user['mobile']
	}
	print('----->  正在检查第<' + str(i + 1) + '/' + length + '>个用户是否审核通过。。。'  )
	r = s.post(basicUrl + 'apply/list/5', params = param)
	#如果正则匹配不到‘无数据’那么就是成功的
	strlist = cer.findall(r.text)
	if len(strlist) == 0:
		successlist.append(user)
		#users.pop(i)
	else:
		checklist.append(user)
print('\n共<' + str(len(successlist)) + '/' + length + '>个用户审核通过\n')

#审核失败的用户

for i,user in enumerate(checklist):
	param = {
		'startTime':'',
		'endTime':'',
		'query':user['mobile']
	}
	print('----->  正在检查第<' + str(i + 1) + '/' + str(len(checklist)) + '>个用户是否审核失败。。。')
	r = s.post(basicUrl + 'apply/list/8', params = param)

	strlist = cer.findall(r.text)
	if len(strlist) == 0:
		cer2 = re.compile('(/qudao/edit_fulfill/\d+)')
		strlist = cer2.findall(r.text)
		if len(strlist) != 0:
			r = s.get('https://qfpay.com' + strlist[0])
			cer3 = re.compile('<p id="id_auditLog">审批信息：(.+?)</p>')
			strlist = cer3.findall(r.text)
			if (len(strlist) != 0):
				remark = strlist[0]
				user['remark'] = remark
				checklist[i] = user
		faillist.append(user)
print('\n共<' + str(len(faillist)) + '/' + length + '>个用户审核失败\n')


#处理审核拒绝的用户
checklist = [i for i in checklist if i not in faillist]
for i,user in enumerate(checklist):
	param = {
		'startTime':'',
		'endTime':'',
		'query':user['mobile']
	}
	print('----->  正在检查第<' + str(i + 1) + '/' + str(len(checklist)) + '>个用户是否审核拒绝。。。')
	r = s.post(basicUrl + 'apply/list/7', params = param)
	#如果正则匹配不到'审核信息'的链接地址，那么就是失败
	#失败的情况需要爬取失败原因
	#如果正则匹配不到‘无数据’那么就是成功的
	strlist = cer.findall(r.text)
	if len(strlist) == 0:
		cer2 = re.compile('(/qudao/auditlog/\d+)')
		strlist = cer2.findall(r.text)
		if len(strlist) != 0:
			r = s.get('https://qfpay.com' + strlist[0])
			cer3 = re.compile('备注</dt>\s+?<dd>(.+?)</dd>')
			strlist = cer3.findall(r.text)
			if (len(strlist) != 0):
				remark = strlist[0]
				user['remark'] = remark
				checklist[i] = user
		refuselist.append(user)
print('\n共<' + str(len(refuselist)) + '/' + length + '>个用户审核拒绝\n')

checklist = [i for i in checklist if i not in refuselist]

#生成exl
print('正在生成导入并修改exl。。。\n')
wbk = xlwt.Workbook()
sheet1 = wbk.add_sheet('sheet 1')

sheet1.write(0,0,'登录账号')
sheet1.write(0,1,'申请状态')
sheet1.write(0,2,'备注')

line = 1
for user in successlist:
	sheet1.write(line, 0, user['custcode'])
	sheet1.write(line, 1, '审核通过')
	line = line + 1

for user in faillist:
	sheet1.write(line, 0, user['custcode'])
	sheet1.write(line, 1, '审核失败')
	sheet1.write(line, 2, user['remark'])
	line = line + 1

for user in refuselist:
	sheet1.write(line, 0, user['custcode'])
	sheet1.write(line, 1, '审核拒绝')
	sheet1.write(line, 2, user['remark'])
	line = line + 1

xlstime = time.strftime(('%Y-%m-%d'))
wbk.save('d:/qfhj/importChange' + xlstime + '.xls')
print('===== d:/qfhj/importChange' + xlstime + '.xls 生成成功 =====\n')

#登录钱包后台，导入exl
postData = '{"username":"用户名","password":"密码"}'

print('再次登录钱包后台。。。\n')
s.post(host + 'yfpay_admin/user/login', data = postData, headers = headers)
print('登录成功！！！\n')

print('导入excel。。。\n')
file = {'reportExcelFile': ('importChange' + xlstime + '.xls', open('d:/qfhj/importChange' + xlstime + '.xls', 'rb'), 'application/vnd.ms-excel')}
s.post(host + 'yfpay_admin/preMerchantapply/importChange', files=file)

print('============ 完成倒入并修改！============\n')

if len(checklist) != 0:
	print('以下用户需要手动查看：')
	for user in checklist:
		print(user['custcode'])

input('\n按回车键退出：')