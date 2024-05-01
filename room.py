from logger import log
from conf import *
from datetime import *
import time
import json
from flask import jsonify


"""
JSON output for /room.
"""
def getStatus():
	try:
		with open(ROOM_STATUS_FILE, 'r') as f:
			return json.loads(f.read())

	except IOError:
		log.exception("Could not read %s." % ROOM_STATUS_FILE)
		message = { 'success': False, 'status': 'Room status record unreadable.' }
		resp = jsonify(message)
		resp.status_code = 500
		return resp
	else:
		f.close()

"""
Boolean
"""
def isRoomOpen():
	return getStatus()["open"]

"""
This method gets called when a new status gets submitted
"""
def submitStatus(open_):
	try:
		with open(ROOM_STATUS_FILE, 'r') as f:
			room = json.loads(f.read())

		if room['open'] != open_:
			with open(ROOM_STATUS_FILE, 'w') as f:

				newStatus = {	'since': int(time.time()),
								'open': open_ }

				addToArchive({'open': open_, 'lastchange': int(time.time())})
				f.write(json.dumps(newStatus))

		return jsonify({ 'success': True })

	except IOError:
		log.exception("Could not read/write %s." % ROOM_STATUS_FILE)
		message = { 'success': False, 'status': 'Room status record unwriteable/unreadable.' }
		resp = jsonify(message)
		resp.status_code = 500
		return resp

def addToArchive(newStatus):
	with open(ROOM_ARCHIVE_FILE, 'r') as f:
		archive = json.loads(f.read())

	archive.append(newStatus)

	with open(ROOM_ARCHIVE_FILE, 'w') as f:
		json.dump(archive, f)
