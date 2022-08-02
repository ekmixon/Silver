import re
import socket

import concurrent.futures

def resolve(hostname):
	if re.search(r'^\d+\.\d+\.\d+\.\d+', hostname):
		return hostname
	try:
		return socket.gethostbyaddr(hostname)[2][0]
	except socket.gaierror:
		return ''

def handler(hostnames):
	threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
	futures = (threadpool.submit(resolve, hostname) for hostname in hostnames)
	ips = {
		result.result()
		for result in concurrent.futures.as_completed(futures)
		if result.result()
	}

	return list(ips)

def resolver(hostnames):
	if type(hostnames) != str:
		return handler(hostnames)
	resolved = []
	with open(hostnames, 'r') as inpfile:
		resolved.extend(iter(inpfile))
	result = set(handler(filter(None, resolved)))
	with open(f'silver-{hostnames}', 'w+') as outfile:
		for ip in result:
			outfile.write(ip + '\n')
	return f'silver-{hostnames}'
