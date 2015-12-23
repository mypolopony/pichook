#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mypolopony
# @Date:   2015-12-20 23:52:10
# @Last Modified by:   mypolopony
# @Last Modified time: 2015-12-22 10:40:23

# TODO:
# For stream: 
# 	for line in tailer.follow(open('/Users/mypolopony/Downloads/irc.undernet.org (DC7C9)/Channels/#0!!!!!!!!!!younggirlsex/2015-12-22.txt')):
#		print(line)

import re
import exifread

# Home for wayward variables
filetype = 'jpg'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
domain = re.compile('(?:http://)([^/]+)')

def writebytes(data,name,filetype):
	with open(name + '.' + filetype,'wb') as o:
		o.write(data)

def getdomain(text):
	return domain.search(text).group(1)

def readexif(filename):
	with open(filename,'rb') as f:
		tags = exifread.process_file(f)
	# For reference, as per http://www.opanda.com/en/pe/help/gps.html
	# tags['GPS GPSLongitude'].values will return degrees, minutes and seconds
	return tags

# Imagevenue
# line = 'http://img173.imagevenue.com/img.php?image=32508_FN015C_123_94lo.JPG'
filename = re.search('(?:=)(.+)',line).group(1)
prefix = re.search('(?:img)+[^.]+',line).group(0)

# First pass
payload = {'image':filename}
uri = 'http://{prefix}.imagevenue.com/img.php'.format(prefix=re.search('img[0-9]+',line).group(0))
r = requests.get(uri,params=payload,headers=headers)

# Second pass
realfilename = re.search('(?:alt=")[^"]+',str(r.content)).group().replace('alt="','')
uri = 'http://{prefix}.imagevenue.com/'.format(prefix=prefix) + realfilename
r = requests.get(uri,headers=headers)
writebytes(r.content,getdomain(line).replace(prefix+'.','') + realfilename,filetype)


# Grusom
# line = 'http://grusom.org/index.php?p=image&id=8582&n=lol2.jpg'
pattern = re.compile('(?:[id=])[0-9]+')

id = pattern.search(line).group(0)[1:]
uri = 'http://grusom.org/p.php'
payload = {'id': id, 't': 'gi'}
r = requests.get(uri,params=payload,headers=headers)
writebytes(r.content,getdomain(line) + id,filetype)