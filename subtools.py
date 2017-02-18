#!/usr/bin/env python3
import re
import os
import sys
import argparse
import requests
from multiprocessing.dummy import Pool as ThreadPool
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

def get_url_signatures(url):
    service_signatures = {
        'Heroku': '<iframe src="//www.herokucdn.com/error-pages/no-such-app.html"></iframe>',
        'GitHub Pages': '<p> If you\'re trying to publish one, <a href="https://help.github.com/pages/">read the full documentation</a> to learn how to set up <strong>GitHub Pages</strong> for your repository, organization, or user account. </p>',
        'Squarespace': '<title>Squarespace - No Such Account</title>',
        'Shopify': '<div id="shop-not-found"> <h1 class="tc">Sorry, this shop is currently unavailable.</h1> </div>',
        'Zendesk': '<span class="title">Bummer. It looks like the help center that you are trying to reach no longer exists.</span>',
        'GitLab': '<head> <title>The page you\'re looking for could not be found (404)</title> <style> body { color: #666; text-align: center; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; margin: 0; width: 800px; margin: auto; font-size: 14px; } h1 { font-size: 56px; line-height: 100px; font-weight: normal; color: #456; } h2 { font-size: 24px; color: #666; line-height: 1.5em; } h3 { color: #456; font-size: 20px; font-weight: normal; line-height: 28px; } hr { margin: 18px 0; border: 0; border-top: 1px solid #EEE; border-bottom: 1px solid white; } </style> </head>'
    }
    data = get_url_data(url)
    if data == 0:
        return []
    #Strip newlines
    data = data.replace('\n', '').replace('\r', '')
    data = re.sub("\s\s+", ' ', data);
    results = []
    for name in service_signatures:
        if service_signatures[name] in data:
            results.append(name)
    return results

def get_url_data(url, timeout=25):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    try:
        resp = requests.Session().get(url, headers=headers, timeout=timeout)
    except Exception:
        resp = None
    if resp is None:
        return 0
    return resp.text if hasattr(resp, "text") else resp.content

def takeover(domain):
		print('Checking '+domain+': ...')
		if len(get_url_signatures(domain)) > 0:
			print('\x1b[6;30;42m [+] ' + domain + '\x1b[0m')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Subdomain netsec tool by radical ed')
	parser.add_argument('-l','--logfile', help='Logfile', required=True)
	parser.add_argument('-s','--sort', help='Sort', action='store_true', required=False)
	parser.add_argument('-c','--check', help='Check if up', required=False, action='store_true')
	parser.add_argument('-v','--verbose', help='Verbose output', required=False, action='store_true', default=False)
	parser.add_argument('-o','--outputFile', help='Output file', required=False, default=False)
	parser.add_argument('-to','--takeover', help='Domain takeover check', required=False, default=False, action='store_true')
	args = vars(parser.parse_args())
	if args['check']:
		dig(args['logfile'], args['outputFile'], args['verbose'])
		
	if args['takeover']:
		domains =  open(args['logfile']).readlines()
		domains = [ domain.strip() for domain in domains ]		
		for i in range(len(domains)):
			if domains[i][-1:] != '/': domains[i]+='/'
			if domains[i][0:4] != "http": domains[i] = "http://" + domains[i]
			
		#for domain in domains:
		#	if domain[-1:] != '/': domain+='/'
		#	if domain[0:4] != "http": domain = "http://" + domain
		pool = ThreadPool(25)  #thread
		results = pool.map(takeover, domains)
		#takeover(domain)
	if args['sort']: sort(args['logfile'])
