from functools import update_wrapper
import json
import time

from flask import request, jsonify

"""
Checks if given parameters are available as GET or POST variables.
"""
def parameters_given(params):
	def decorator(fn):
		def wrapped_function(*args, **kwargs):
			for param in params:
				if request.method == 'POST' and not paramExists(param):
					message = { 'success': False, 'status': 'Please define all non-optional arguments.' }
					resp = jsonify(message)
					resp.status_code = 403
					return resp

			return fn(*args, **kwargs)
		return update_wrapper(wrapped_function, fn)
	return decorator

def getParam(name):
	return request.form[name]

def paramExists(param):
	return param in request.form

"""
Determine whether a string represents a boolean true or false.
"""
def isTrue(param):
	if param.lower() == 'true' or param == '1':
		return True
	elif param.lower() == 'false' or param == '0':
		return False
	else:
		raise TypeError("Parameter could not be converted to boolean.")

"""
General http errors
"""
# FIXME: use some kind of global conversion of error messages (to json)
def error405():
	resp = jsonify({'success': False, 'status': 'Method not allowed.'})
	resp.status_code = 405
	return resp

def error504():
	resp = jsonify({'success': False, 'status': 'Time-out reached.'})
	resp.status_code = 504
	return resp

"""
Returns dictionary with requested status info.
"""
def getStatus(filename):
	with open(filename, 'r') as f:
		status = json.loads(f.read())
		return status

"""
Updates given status info.
"""
def setStatus(filename, newStatus, lastMeasure=False):
	oldStatus = getStatus(filename)
	lastUpdate = oldStatus["lastUpdate"]
	try:
		del oldStatus["lastUpdate"]
		del oldStatus["lastMeasurement"]
	except KeyError:
		pass
	if oldStatus != newStatus:
		newStatus["lastUpdate"] = int(time.time())
	if lastMeasure:
		# last measurement: now
		newStatus["lastMeasurement"] = int(time.time())
		if "lastUpdate" not in newStatus:
			# recover lastUpdate
			newStatus["lastUpdate"] = lastUpdate

	# update or measurement enabled? write!
	if oldStatus != newStatus:
		with open(filename, 'w') as f:
			f.write(json.dumps(newStatus))

	return { 'success': True }
