#!/usr/bin/env python
import urllib2
import argparse 
import sys
import time
''' HTTP fuzzer by Radical Ed '''


def url_exists(location):
	request = urllib2.Request(location)
	request.get_method = lambda : 'HEAD'
	try:
		response = urllib2.urlopen(request)
		print('[+] '+location)
		return True
	except urllib2.HTTPError:
		return False

def fuzzer(domain, wordlist='/home/ed/dev/wordlists/web.txt'):
	if domain[-1:] != '/': domain+='/'
	if domain[0:4] != "http": domain = "http://" + domain
	wordlist = open(wordlist).readlines()
	wordlist = [x.strip() for x in wordlist]
	for word in wordlist:
		url_exists(domain+word)

	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Python web fuzzer')
	parser.add_argument('-d','--domain', help='Domain', required=True)
	parser.add_argument('-w','--wordlist', help='Sort', required=False)
	parser.add_argument('-o','--output', help='Output file', required=False)
	args = vars(parser.parse_args())
	if args['wordlist']:
		fuzzer(args['domain'], args['wordlist'])
	else:
		fuzzer(args['domain'])
