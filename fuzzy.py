#!/usr/bin/env python3
import urllib.request
import argparse 
import sys
import os
import time
from multiprocessing.dummy import Pool as ThreadPool 
global args
global wordlist
global successful
successful = []
''' HTTP fuzzer by Radical Ed '''

def url_exists(location):
	request = urllib.request.Request(location)
	request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
	request.get_method = lambda : 'HEAD'
	try:
		response = urllib.request.urlopen(request, timeout=1)
		return True
	except:
		if args['verbose']: print('[-] '+location)
		return False


def fuzzer(domain):
	if domain[-1:] != '/': domain+='/'
	if domain[0:4] != "http": domain = "http://" + domain
	for word in wordlist():
		url = domain+word
		if url_exists(url):
			if args['verbose']: print('\x1b[6;30;42m [+] ' + url + '\x1b[0m')
			successful.append(url)
		else:			
			if args['verbose']: print('[-] ' + url)

def wordlist():
	path = ''
	if args['wordpress']:
		path = '/home/ed/dev/wordlists/wordpress.txt'
	else:
		path = args['wordlist']
	dictionary = open(path).readlines()
	dictionary = [ word.strip() for word in dictionary ] # remove '\r' and '\n'
	return dictionary
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Python web fuzzer')
	parser.add_argument('-l','--logfile', help='File full of target domains', required=False)
	parser.add_argument('-w','--wordlist', help='Sort', required=False)
	parser.add_argument('-o','--output', help='Output file', required=False)
	parser.add_argument('-v','--verbose', help='Verbose mode', required=False, action='store_true')
	parser.add_argument('-wp','--wordpress', help='Wordpress mode', required=False, action='store_true')
	
	
	
	args = vars(parser.parse_args())
	
	domains = open(args['logfile']).readlines()
	domains = [ hostname.strip() for hostname in domains ] 
		
	pool = ThreadPool(13)  #thread
	results = pool.map(fuzzer, domains)
		
	#results
	successful.sort()
	for success in successful: 
		print('\x1b[6;30;42m [+] ' + success + '\x1b[0m')
	if args['output']:
		logfile = open(args['output'], 'a')
		for success in successful: logfile.write(success+'\n')
		logfile.close()

