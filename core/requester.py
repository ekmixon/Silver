import warnings
import requests

warnings.filterwarnings('ignore') # Disable SSL related warnings

def requester(url, get=True, data={}):
    return (
        requests.get(url, params=data, verify=False)
        if get
        else requests.post(url, data=data, verify=False)
    )
