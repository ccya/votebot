# -*- coding:utf-8 -*-
import json
import os
import re
import subprocess
import sys
import votebotAbu

from datetime import datetime
from pytz import timezone


def stop():
	# stop votebot
	ps = subprocess.Popen(('ps', '-A'), stdout=subprocess.PIPE)
	pid = subprocess.check_output(('grep', 'python service.py start'), stdin=ps.stdout)
	os.system("kill -9 "+ str(pid))

	# analyze log file
	log = open("votebotAbu.log","r")
	lines = log.readlines()
	log.close()
	voteDic = {}
	msgDic = {}
	for i in xrange(len(lines)):
		if i==0:
			first_line = lines[i]
		tags = re.findall("\[(.*?)\]",lines[i])
		if "INFO" != tags[0]:
			fl.write(lines[i])
		result = json.loads("{" + re.findall(r'\{(.+?)\}', lines[i])[0] + "}")
		if str(result['errorno']) in voteDic:
			voteDic[str(result['errorno'])] += 1
		else:
			voteDic[str(result['errorno'])] = 1
			msgDic[str(result['errorno'])] = result['msg'].encode('utf-8')

	# write to new file
	parsedTime = re.findall("\[(.*?)\]",first_line)[1]
	startDatetime = datetime.strptime(parsedTime, "%Y-%m-%d %H:%M:%S,%f")
	starttime = str(startDatetime.month) + str(startDatetime.day) + str(startDatetime.hour) + str(startDatetime.minute)+ str(startDatetime.second)
	endDatetime = datetime.now(timezone('America/Los_Angeles'))
	endtime = str(endDatetime.month) + str(endDatetime.day) + str(endDatetime.hour) + str(endDatetime.minute)+ str(endDatetime.second)
	filename = "votebotAbu"+str(starttime)+"_"+str(endtime)+ ".log"
	fl = open(filename, 'a+')
	for k, v in voteDic.items():
		msg = " ".join([k,str(voteDic[k]),msgDic[k]])
		fl.write(msg+"\n")
	fl.close()

	# rename old file
	os.rename("votebotAbu.log","votebotAbu"+endtime)


def start():
	votebotAbu.VoteBot().starter()

def main():
	arg = sys.argv
	if  "start" == arg[1]:
		start()
	elif "stop" == arg[1]:
		stop()

if __name__ == "__main__":
    main()
		


