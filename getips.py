#!/usr/bin/env python

import argparse 

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Tool to isolate ips from Aquatones host report')
	parser.add_argument('hostfile', help='aquatone host file')
	args = vars(parser.parse_args())
	if args['hostfile']:
		hostfile = open(args['hostfile'],'r').readlines()
	hostfile.sort()
	ips = []
	for i in hostfile:
		ips.append(i.split()[0])
	ips = list(set(ips)) #remove duplicates
	ips.sort()
	newfile = open('ips-'+args['hostfile'],'a')
	for i in ips:
		newfile.write(i+'\n')
	newfile.close()
	print('Output saved to: ips-'+args['hostfile'])