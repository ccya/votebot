# -*- coding:utf-8 -*-
import urllib2
import urllib
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.keys import Keys
import logging
import datetime


class VoteBot:
	def __init__(self):
		surfix = datetime.datetime.now().strftime('%m-%d')
		logfile = 'VoteBot'+surfix
		logging.FileHandler(logfile)
		self.proxySource = "http://cn-proxy.com/"
		self.proxyList = []
		self.userAgents = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWe...chrome/45.0.2454.101 Safari/537.36",
		"Mozilla / 5.0(Windows NT 6.1) AppleWebKit / 537.....likeGecko) Chrome / 45.0.2454.101Safari/ 537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit.....Gecko) Chrome/50.0.2661.102 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3....ML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
		"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...WebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
		"User-Agent: Mozilla/5.0 (Windows NT 10.0) AppleWebKi.....36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) Apple.....KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
		]
	
	def getProxy(self):
		req = urllib2.Request(self.proxySource)
		try: 
			response = urllib2.urlopen(req)
			html = response.read()
			soup = BeautifulSoup(html,"html.parser")
			tables = soup.select(".sortable")
			for table in tables:
				rows = table.find_all('tr')
				for i in xrange(2,len(rows)):
					cols = rows[i].find_all('td')
					ip = (cols[0].string + ":" + cols[1].string).encode('utf-8')
					styles = cols[3].div.strong['style']
					bkground = styles.split(";")[1].split(":")[1]
					if bkground == "#00dd00":
						self.proxyList.append(ip)
						logging.debug("[getProxy]" + ip)	

		except urllib2.URLError as e:
			logging.error(e.reason)
		#email me?
			# quit()

	def vote(self,proxy,userAgent):
		logging.debug("[vote]ip: " + proxy)
		driver = webdriver.Firefox(proxy=Proxy({
			'proxyType': ProxyType.MANUAL,
			'httpProxy': proxy,
			'ftpProxy': proxy,
			'sslProxy': proxy,
			'noProxy': '' # set this value as desired
			}))
		driver.get("http://henan.sina.com.cn/city/zt/zmrmtjy/index.shtml")
		elem = driver.find_element_by_css_selector('.tablist li:nth-child(10)')
		elem.click()
		candidate = driver.find_element_by_css_selector('.toupiaolist li:nth-child(4) div')

		voteButton = candidate.find_element_by_css_selector('a.toupiao')
		voteButton.click()
		driver.close()

	def controller(self):
		self.getProxy()
		for ip in self.proxyList:
			self.vote(ip,random.choice(self.userAgents))
	
		
bot = VoteBot()
bot.controller()
