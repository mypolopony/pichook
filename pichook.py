#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mypolopony
# @Date:   2015-12-20 23:52:10
# @Last Modified by:   mypolopony
# @Last Modified time: 2016-01-15 01:42:21

# TODO:
# For stream: 
# 	for line in tailer.follow(open(filename)):
#		print(line)
#
# Domains:
# Imagetwist: Probably not worth it, most of these seem bunk
# Picpaste: I imagine this might be well guarded

import re
import exifread
import glob
import operator
import logging
import requests
import datetime

# Home for wayward global variables
filetype = 'jpg'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
domain = re.compile('(?:http://)([^/]+)')
timeformat = '%Y-%m-%d%H:%M:%S%Z'
logging.basicConfig(filename='{tf}.log'.format(tf=datetime.date.today().strftime(timeformat)),level=logging.DEBUG)

def writebytes(data,name,filetype):
	with open(name + '.' + filetype,'wb') as o:
		o.write(data)

def getdomain(text):
	if 'imagevenue.com' in text:
		dom = 'imagevenue.com'
	else:
		dom = domain.search(text).group(1)

	return dom

def readexif(filename):
	with open(filename,'rb') as f:
		tags = exifread.process_file(f)
	# For reference, as per http://www.opanda.com/en/pe/help/gps.html
	# tags['GPS GPSLongitude'].values will return degrees, minutes and seconds
	return tags

def imagevenue(url):
	# url = 'http://img173.imagevenue.com/img.php?image=32508_FN015C_123_94lo.JPG'
	filename = re.search('(?:=)(.+)',url).group(1)
	prefix = re.search('(?:img)+[^.]+',url).group(0)

	# First pass
	payload = {'image':filename}
	uri = 'http://{prefix}.imagevenue.com/img.php'.format(prefix=re.search('img[0-9]+',url).group(0))
	r = requests.get(uri,params=payload,headers=headers)

	# Second pass
	realfilename = re.search('(?:alt=")[^"]+',str(r.content)).group().replace('alt="','')
	uri = 'http://{prefix}.imagevenue.com/'.format(prefix=prefix) + realfilename
	r = requests.get(uri,headers=headers)

	shortfn = realfilename.split('/')[-1].lower().replace('.jpg','')
	writebytes(r.content,getdomain(getdomain(url)) + '/' + shortfn, filetype)

	logging.debug('Wrote: {fn}'.format(fn = shortfn))

def grusom(url):
	# url = 'http://grusom.org/index.php?p=image&id=8582&n=lol2.jpg'
	pattern = re.compile('(?:[id=])[0-9]+')

	id = pattern.search(url).group(0)[1:]
	uri = 'http://grusom.org/p.php'
	payload = {'id': id, 't': 'gi'}
	r = requests.get(uri,params=payload,headers=headers)
	writebytes(r.content,getdomain(url) + '/' + id,filetype)

def rawlink(url):
	# url = 
	r = requests.get(url)
	writebytes(r.content,'raw/' + url.split('/')[-1])

def main():
	# This is as particular setup for the Textual client's file structure and my
	# personal setup
	baseurl = '/Users/mypolopony/Downloads'
	server = 'irc.undernet.org'
	sources = glob.glob('{base}/{sv}*/Channels/**/*.txt'.format(base=baseurl,sv=server))

	domainset = dict()

	pattern = 'http:\/\/[^ |\\\n|\)]+'	# extract potential links
	httpfind = re.compile(pattern)
	for so in sources:
		with open(so,'r') as logfile:
			for line in logfile:
				link = httpfind.search(line)
				if link:
					link = link.group(0)
					if filetype in link:
						domain = getdomain(link)

						# Stupid imagevenue subdomain hack
						# This could probably be much bette

						if domain in domainset.keys():
							domainset[domain] += 1
						else:
							domainset[domain] = 1

						if 'grusom.org' in domain:
							#grusom(link)
							pass
						elif 'imagevenue.com' in domain:
							imagevenue(link)
						else:
							pass
							'''
							try:
								rawlink(link)
							except:
								logging.warning('Rawlink failed: {l}'.format(l=link))
							'''

	domainset = sorted(domainset.items(), key=operator.itemgetter(1), reverse=True)
	logging.info('Total Tally:')
	for ds in domainset:
		logging.info('{d}:\t{num}'.format(d=ds[0], num=ds[1]))


if __name__ == '__main__':
    main()