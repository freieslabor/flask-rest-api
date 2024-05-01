from flask import Flask, request, jsonify, render_template
from conf import *
from auth import requires_auth
from httpaccesscontrol import crossdomain
from misc import parameters_given, getParam
import info, room
from flask.ext.cache import Cache

app = Flask(__name__)
app.url_map.strict_slashes = False
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_THRESHOLD': 10})

"""
Error handlers
"""
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

"""
API methods
"""
@app.route('/api')
def api_root():
	return render_template('welcome.html')

"""
Submit/get room status information.
"""
@app.route('/api/room', methods=['GET', 'POST'])
@parameters_given(['people'])
@crossdomain(origin='*')
@requires_auth(True)
def api_room():
	if request.method == 'POST':
		people = getParam('people')
		return room.submitStatus(people)
	elif request.method == 'GET':
		return jsonify(room.getStatus())

"""
Get general information + room status.
"""
@app.route('/api/room_extended')
@app.route('/api/info')
@crossdomain(origin='*')
def api_info():
	return jsonify(info.info())

"""
Server for testing purposes.
"""
if __name__ == '__main__':
	from gevent import pywsgi
	import sys
	pywsgi.WSGIServer(('', 8000), log=sys.stdout).serve_forever()
