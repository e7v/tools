#!/usr/bin/env python3

import os
import sys
import argparse
from random import randint
from termcolor import colored
clean = []


def sort(logfile):
	# only works with dnsscan logs
#	if logfile:
#		logfile = open(logfile).readlines()
#		logfile = [i.strip() for i in logfile]
#		cleaned = [i.split('-') for i in logfile]
#		cleaned.sort()
		#for i in cleaned: print(i[0] + "	" + i[1])
	logfile = open(logfile).readlines()
	logfile = [i.strip() for i in logfile]
	logfile = [i.split('\t') for i in logfile]
	for i in logfile: i.reverse()
	logfile.sort()
	for i in logfile: print(i)
	


def ping(hostname): 
	response = os.system("ping -c 1 -t 1 " + hostname + " &> /dev/null")
	#and then check the response...
	if response == 256:
	  return True
	else:
	  return False

def check(hostsfile, outputlog):
	clean = ''
	hostnames = open(hostsfile, 'r').readlines()
	for host in hostnames:
		if ping(host):
			clean += host
	print(clean)
	open(outputlog, 'w').write(clean)
	return clean
	
def dig(subdomains, logfile=False, verbose=False):
	colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
	if logfile: logfile = open(logfile, 'w')
	subdomains = open(subdomains, 'r').readlines()
	clean = []
	print("\n[*] Working ...", end="")
	for i in subdomains:
		if True:
			clean.append(os.popen('dig +noall +answer ' + i).read())
			#clean.append(os.popen('curl -k -I https://%s/?x=bugbounty' % i))
		print(colored('.', colors[randint(0,len(colors)-1)]), end="", flush=True)
	print('\n', end='')

	clean.sort()
	
	if verbose: 
		for i in clean: print(i)
	if logfile:
		for i in clean:
			logfile.write(i+'\n')
		logfile.close()
	else: return clean


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Subdomain netsec tool by radical ed')
	parser.add_argument('-l','--logfile', help='Logfile', required=True)
	parser.add_argument('-s','--sort', help='Sort', action='store_true', required=False)
	parser.add_argument('-c','--check', help='Check if up', required=False, action='store_true')
	parser.add_argument('-v','--verbose', help='Verbose output', required=False, action='store_true', default=False)
	parser.add_argument('-o','--outputFile', help='Output file', required=False, default=False)
	args = vars(parser.parse_args())
	if args['check']:
		dig(args['logfile'], args['outputFile'], args['verbose'])
	if args['sort']: sort(args['logfile'])
