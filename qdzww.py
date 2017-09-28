# -*- coding: utf-8 -*-  
from __future__ import unicode_literals 
from bs4 import BeautifulSoup
import sys
import urllib
import MySQLdb
import urllib2
import os
import re

reload(sys)
sys.setdefaultencoding('utf-8')
base_protocol = 'https:'

# 获取图书概览信息
def get_book_list(url):
	try:
		request = urllib2.Request(url,headers=headers)
		response = urllib2.urlopen(request)
		#fp = open('1.txt','wb')
		#fp.write(response.read().decode('utf-8').encode('gbk'))
		
		content = response.read()
		# pattern = re.compile('<div.*? class="book-img-text">(.*?)<li.*? data-rid=.*?>(.*?)</li></div>')
		pattern = re.compile('<li data-rid=.*?>(.*?)</li>')
	  	result = re.findall(pattern,content)
		# fp = open('qdzww.txt','wb')

		for item in result:
			soup = BeautifulSoup(item)
			# fp.write(soup.h4.a.string)
			# fp.write('\n')
			author = soup.find_all('p',class_='author')[0].img.a.string
			# fp.write(author)
			# fp.write(soup.a.img['src'])
			# fp.write('\n')
			# info = soup.find_all('p',class_='intro')[0]   #一般用于只有一个属性要求  
			info = soup.find_all(attrs={'class':'intro'})[0]   # 可以用于多个参数
			# fp.write(info.string)
			# fp.write('\n')
			sql = "insert into t_book_list(book_name,book_author,book_pic,book_info,book_link,book_id) values(%s,%s,%s,%s,%s,%s)"
			cur.execute(sql,(soup.h4.a.string,author,base_protocol+soup.a.img['src'],info.string.strip(),base_protocol+soup.a['href'],soup.a['data-bid']))

			# 保存图书目录信息
			get_book_catalog(base_protocol+soup.a['href']+'#Catalog',soup.a['data-bid'])
	
		print("<<<<<coplate!!!!>>>>>>")
	except urllib2.URLError, e:
		if hasattr(e,'cdoe'):
			print(e.code)
		if hasattr(e,'reason'):
			print(e.reason)

# 获取图书章节目录
def get_book_catalog(url,book_id):
	try:
		# url = "https://book.qidian.com/info/1003354631#Catalog"
		# url = "https://book.qidian.com/info/1004608738#Catalog"
		print(url)
		request = urllib2.Request(url,headers=headers)
		response = urllib2.urlopen(request)
		#fp = open('1.txt','wb')
		#fp.write(response.read().decode('utf-8').encode('gbk'))
		
		content = response.read().encode("utf-8")
		fp = open('catalog_temp.txt','wb')
		fp.write(content)
		soup = BeautifulSoup(content)
		volume_set = soup.find_all('div',class_='volume-wrap')[0].find_all('div',class_='volume')
		for volume in volume_set:
			cf_set = volume.find_all('ul',class_='cf')
			for cf in cf_set:
				li_set = cf.find_all('li')
				for li in li_set:
					sql = "insert into t_book_catalog(catalog_name,catalog_info,catalog_link,book_id) values(%s,%s,%s,%s)"
					cur.execute(sql,(li.a.string,li.a['title'],base_protocol+li.a['href'],book_id))
	    # print("<<<<<complate!!!!>>>>>>")
	except urllib2.URLError, e:
		if hasattr(e,'cdoe'):
			print(e.code)
		if hasattr(e,'reason'):
			print(e.reason)
	except Exception :
		print('exception.....')
 

#url = "http://www.qiushibaike.com/hot/page/2/"
# url = "https://www.qidian.com/all"
base_url = "https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&hiddenField=0&page="
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
conn = MySQLdb.connect(
		host='localhost',
		port = 3306,
		user = 'root',
		passwd = '378541',
		db = 'python',
		charset='utf8')
cur = conn.cursor()
pages = range(1,2)
for page in pages:
	# print(page)
	url = base_url + str(page)
	print(url)
	get_book_list(url)
# get_book_catalog("aaa",11)
cur.close()	
conn.commit()
conn.close()



#  add to git  2017年9月28日23:28:38











