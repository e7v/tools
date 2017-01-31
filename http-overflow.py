#!/usr/bin/env python

import os
import sys

def curl(host="https://suse/", payload=4016, extra=''):
	payload = "+" * int(payload)
	print os.popen('curl -L -I %s?x=%s%s' % (host, payload, extra)).read()

if __name__ == "__main__": 
	try: 
		hostname = sys.argv[1]
		payload = sys.argv[2]
		try: extra = sys.argv[3]
		except: extra = ''
		curl(hostname, payload, extra)
	except:
		print "Usage: overflow.py [hostname] [byte size] [extra]"
	
	
