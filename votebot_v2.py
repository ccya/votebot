# -*- coding:utf-8 -*-
import urllib2
import urllib
import random
from bs4 import BeautifulSoup
import logging
import json

class VoteBot:
	def __init__(self):
		self.totalVote = 0
		logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s',filename='votebot.log',level=logging.DEBUG)
		logging.info("[init] starting a new voting round")
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
			response.close()
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

	def getProxy2(self):
		for i in xrange(1,11):
			try:
				req = urllib2.Request("http://www.kuaidaili.com/proxylist/" + str(i))
				response = urllib2.urlopen(req)
				html = response.read()
				response.close()
				soup = BeautifulSoup(html,"html.parser")
				table = soup.select("#index_free_list")[0]
				rows = table.find_all('tr')
				for i in xrange(1,len(rows)):
					cols = rows[i].find_all('td')
					ip = (cols[0].string + ":" + cols[1].string).encode('utf-8')
					self.proxyList.append(ip)
					logging.debug("[getProxy2]" + ip)
			except urllib2.URLError as e:
				logging.error(e.reason)

	def vote(self,proxy,userAgent):
		# http://sinahn.cc/Index/doTJYVoting?wid=7369427&callback=jQuery17105178477708445559_1474271335103&_=1474274701840
		urlPram = urllib.urlencode({
				'wid':'7369427',
				'callback':'jQuery17105178477708445559_1474271335103',
				'_':'1474274701840'
				})
		voteUrl = 'http://sinahn.cc/Index/doTJYVoting?'
		req = urllib2.Request(voteUrl + urlPram)
		req.add_header("User-Agent",userAgent)
		req.add_header("Referer",'http://henan.sina.com.cn/city/zt/zmrmtjy/index.shtml')
		req.add_header("Host",'sinahn.cc')

		proxy_support = urllib2.ProxyHandler({"http":proxy})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		try:
			votePage = urllib2.urlopen(req,timeout=8)
			s = votePage.read()
			votePage.close()
			result = s[s.find("(")+1:s.find(")")]
			logging.debug("[vote]ip: " + proxy + " result: " + result)
			self.totalVote+=1
		except Exception as e:
			logging.error("[vote]ip: "+ proxy)
			logging.error(e)
		
	def controller(self):
		self.getProxy()
		self.getProxy2()
		logging.info("[controller]total proxy: " + str(len(self.proxyList)))
		for ip in self.proxyList:
			self.vote(ip,random.choice(self.userAgents))
		logging.info("[controller]totalvote: " + str(self.totalVote))


		
bot = VoteBot()
bot.controller()
