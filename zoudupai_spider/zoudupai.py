import requests
import random
from bs4 import BeautifulSoup
import re

base_url = 'http://www.zoudupai.com'
s = requests.Session()

urlCer = re.compile('.*?\(\'(.*?mobi)', flags = 0)
titleCer2 = re.compile('.*?《(.*?)》', flags = 0)

r = s.get(base_url + '/hot/1')
soup = BeautifulSoup(r.text, "lxml")
books = soup.div.find_all('div', 'modify')
dict = {}
for book in books:
	urlText = book.div.contents[1]
	if len(urlCer.findall(urlText))>0:
		url = urlCer.findall(urlText)[0]
		titleText = book.find('div', 'title-sign').p.string
		titleCer = re.compile('.*?《(.*?)》', flags = 0)
		if len(titleCer.findall(titleText)):
			title = titleCer.findall(titleText)[0].strip()
			dict[title] = url

page_no = 2

hasNextPage = 1

while hasNextPage == 1:

	get_param = {
		'm': 'index',
		'a': 'share',
		'width': '190',
		'p': page_no,
		'cate': '1',
		'v': '10247626.008861544'
	}

	r = s.get(base_url + '/services/service.php', params = get_param)

	books  = r.json()['result']
	hasNextPage = r.json()['hasNextPage']

	def downloadUrl(tag):
	    return tag.has_attr('onclick') and tag.name == 'div'


	for book in books:
		r = s.get(base_url + book['share_url'])
		soup = BeautifulSoup(r.text, "lxml")
		urlText = soup.div.find_all(downloadUrl)[0]['onclick']
		if len(urlCer.findall(urlText))>0:
			url = urlCer.findall(urlText)[0]
			titleText = soup.title.string
			titleCer = re.compile('.*?《(.*?)》', flags = 0)
			if len(titleCer.findall(titleText)):
				title = titleCer.findall(titleText)[0].strip()
				dict[title] = url

	page_no = page_no + 1

for k,v in dict.items():
	r = s.post(base_url + v)
	with open(k.replace('*','X').replace(':','：') + '.mobi', 'wb') as f:
		f.write(r.content)