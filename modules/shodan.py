from core.colors import good
from core.utils import notify
from core.requester import requester

def shodan(ips, exclude):
	result = {}
	for ip in ips:
		if ip in exclude and exclude[ip].get('vuln', False):
			message = f'{ip} has a vulnerable service'
			notify(f'[Vuln] {message}')
			print(f'{good} {message}')
			continue
		result[ip] = {'source': 'shodan'}
		data = requester(f'https://internetdb.shodan.io/{ip}').json()
		if '"No information available"' in data:
			continue
		elif data['vulns']:
			result[ip]['vuln'] = True
			message = f'{ip} has a vulnerable service'
			notify(f'[Vuln] {message}')
			print(f'{good} {message}')
		result[ip]['ports'] = {port: {'state': 'open'} for port in data['ports']}
	return result
