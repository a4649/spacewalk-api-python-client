import datetime
import re
import xmlrpclib

SATELLITE_URL = "http://127.0.0.1/rpc/api" # replace with IP of your Spacewalk / Satellite Server
SATELLITE_LOGIN = "api-user"
SATELLITE_PASSWORD = "api-user-password"
TIMEOUT = 900

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)


	
def login():
	'''
	Request session cookie
	
	Returns:
		string: Sessio ID (cookie). Null if login failed.
	'''
	try:
		key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
		return key
	except Exception as ex:
		pprint 'Error connecting to spacewalk: {}'.format(ex)
		return None

def logout(session_key):
	"""Request to destroy session cookie
	Args:
		session_key (str): Session ID (cookie)
	Returns:
		str: OK if success, Error if fails
	"""
	try:
		tkey = client.auth.logout(session_key)
		if tkey == 1:
			logging.info('OK')
	except Exception as ex:
		print ('Error terminating session from spacewalk: {}'.format(ex))

def show_users(session_key):
	"""Show spacewalk users

	Args:
		session_key (str): Session ID (cookie)

	Returns:
		list(str): List of spacewalk usernames
	"""
	print client.user.list_users(session_key)

def show_api_version():
	"""Show spacewalk API version

	Returns:
		float: XMLRPC API version
	"""
	print client.api.getVersion()

def show_sat_version():
	"""Show spacewalk / satellite version

	Returns:
		float: Satteline version
	"""
	print client.api.systemVersion()

def get_systems(session_key, pattern):
	"""Get system matching pattern 

	Args:
		session_key (str): Session ID (cookie)

	Returns:
		list(int): ID's of the systems matched by the pattern
	"""
	systems_list = []
	systems = client.system.listUserSystems(session_key, SATELLITE_LOGIN)
	for system in systems:
		if re.match(r'{}.*'.format(pattern), system['name']):
			systems_list.append(system['id'])	
		else:
			continue	
	return systems_list	

def run_script(session_key, label, target, uid, gid, script):
	"""Schedule action to run script

	Args:
		session_key (str): Session ID (cookie)
		label (str): Label for the action
		target array(str): ID's of the systems to run the script
		uid (str): user to run the script
		gid (str): group to run the script
		script (str): script to run

	Returns:
		string: Action ID if scheduled action succeed, Error message if it goes wrong
	"""
	try:
		action_id = client.system.scheduleScriptRun(session_key, label, target, uid, gid, TIMEOUT, script, datetime.datetime.now())
		if action_id:
			print('Successfully scheduled action number {}'.format(action_id))
	except Exception as ex:
		print ('Error scheduling action:\n{}'.format(ex))
