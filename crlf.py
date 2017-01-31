#!/usr/bin/env python3
'''check for CRLF'''
from __future__ import print_function
import os
import sys
import argparse
from termcolor import colored
#from __future__ import print_function

payloads = open('/home/ed/dev/wordlists/crlf.txt').readlines()

def targets(hosts):
	try:
		hosts = open(hosts).readlines()
		hosts = [host.strip() for host in hosts]
		return hosts
	except: pass
def curl(hostname='', payload=''):
	
		
	try: payload = sys.argv[2]
	except: pass
	

	for payload in payloads:
		response = os.popen('''curl --connect-timeout 1 -k -I "%s%s" --max-time 2 &> /dev/stdout | grep Location''' % (hostname, payload.strip())).read()
		print('.', end="")
		if 'Location' in response: 
			#print(colored(response, 'red'))
			print('[+] ' + hostname + payload.strip())
#		elif 'google' in response: print colored(response, 'red')
#		elif 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx': print response
#		elif 'crlftest' in response: print response
#		elif 'Location: http://makingvimeo.com' in response: 
#			print colored("DING DING DING!!!!!!!!!", 'red')*10

if __name__ == "__main__": 
	parser = argparse.ArgumentParser(description='CRLF fuzzer by ed')
	parser.add_argument('-l','--hostsfile', help='Hostsfile', required=False)
	parser.add_argument('-s','--single', help='Single', required=False, action='store_true')
#	parser.add_argument('-c','--check', help='Check if up', required=False)
	parser.add_argument('-o','--output', help='Output file', required=False)
	args = vars(parser.parse_args())
	
	if args['hostsfile']:
	    for hostname in targets(args['hostsfile']):
	        if hostname[-1:] != '/': hostname+='/' #append '/' to url    
	        curl(hostname)
	        if hostname[:5] != 'https': 
	            if hostname[-1:] != '/': hostname+='/' #append '/' to url
	            hostname = 'https://' + hostname
	            curl(hostname)
	else:
		print("Usage: crlf.py -l [hostname]")

