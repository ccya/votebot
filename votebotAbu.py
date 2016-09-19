# -*- coding:utf-8 -*-
import urllib2
import urllib
import random
import logging
import json
import threading


class VoteBot:
	def __init__(self):
		self.totalVote = 0
		logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s',filename='votebot.log',level=logging.INFO)
		self.proxyList = []
		self.userAgents = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWe...chrome/45.0.2454.101 Safari/537.36",
		"Mozilla / 5.0(Windows NT 6.1) AppleWebKit / 537.....likeGecko) Chrome / 45.0.2454.101Safari/ 537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit.....Gecko) Chrome/50.0.2661.102 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3....ML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
		"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...WebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
		"User-Agent: Mozilla/5.0 (Windows NT 10.0) AppleWebKi.....36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) Apple.....KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
		]

	def vote(self,userAgent):
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

		proxyHost = "proxy.abuyun.com"
		proxyPort = "9010"
		proxyUser = "H75L3ZTG3Y5E315P"
		proxyPass = "2362FFBD452BCE33"
		proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
			"host" : proxyHost,
			"port" : proxyPort,
			"user" : proxyUser,
			"pass" : proxyPass,
		}
		proxy_handler = urllib2.ProxyHandler({
			"http"  : proxyMeta,
			"https" : proxyMeta,
		})
		opener = urllib2.build_opener(proxy_handler)
		opener.addheaders = [("Proxy-Switch-Ip", "yes")]
		urllib2.install_opener(opener)
		try:
			votePage = urllib2.urlopen(req,timeout=5)
			s = votePage.read()
			votePage.close()
			result = s[s.find("(")+1:s.find(")")]
			logging.info("[vote]result: " + result)
			self.totalVote+=1
		except Exception as e:
			logging.debug(e)
		
	def controller(self):
		logging.info("[controller]start voting")
		self.vote(random.choice(self.userAgents))

		
bot = VoteBot()
bot.controller()
