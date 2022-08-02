import time

from core.requester import requester
from core.utils import write_json, load_json

file = './db/vulners_cache.json'

database = load_json(file)
current_time = int(time.time())
if 'time' not in database or (current_time - database.get('time', 0)) > 86400:
    database = {'by_cpe':{}, 'by_version':{}}
database['time'] = current_time

def vulners(software, version, cpe=False):
    if not software or not version:
        return False
    if cached := query_cache(software, version, cpe):
        return cached == 'vulnerable'
    kind = 'cpe' if cpe else 'software'
    data = '{"software": "%s", "version": "%s", "type" : "%s", "maxVulnerabilities" : %i}' % (software, version, kind, 1)
    response = requester('https://vulners.com/api/v3/burp/software/', get=False, data=data).text
    cache(software, version, response, cpe)
    return 'Nothing found for Burpsuite search request' not in response

def query_cache(software, version, cpe):
    if cpe:
        if software in database['by_cpe']:
            return (
                'vulnerable'
                if database['by_cpe'][software] == True
                else 'not-vulerable'
            )

    elif software in database['by_version']:
        if version in database['by_version'][software]:
            return (
                'vulnerable'
                if database['by_version'][software][version] == True
                else 'not-vulerable'
            )

        else:
            return False
    return False

def cache(software, version, response, cpe):
    vulnerable = 'Nothing found for Burpsuite search request' not in response
    if cpe:
        if software not in database['by_cpe']:
            database['by_cpe'][software] = vulnerable
    else:
        if software not in database['by_version']:
            database['by_version'][software] = {}
        if version not in database['by_version'][software]:
            database['by_version'][software][version] = vulnerable
    write_json(file, database)
