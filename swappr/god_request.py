import os
import requests

god_session = requests.Session()
god_session.headers.update({
	'Authorization': 'bearer ' + os.environ['SWAPPR_TANDA_GOD_TOKEN'],
	'Content-Type': 'application/json'
})

def get(path):
	return god_session.get('https://my.tanda.co/api/v2/' + path)

def put(path, data=None):
	return god_session.put('https://my.tanda.co/api/v2/' + path, data=data)