#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template, send_file
from flask_caching import Cache

from .conf import *
from .auth import requires_auth
from .httpaccesscontrol import crossdomain
from .misc import parameters_given, getParam, isTrue
from .info import info
from .room import isRoomOpen, getStatus, submitStatus

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
@parameters_given(['open'])
@crossdomain(origin='*')
@requires_auth(True)
def api_room():
	if request.method == 'POST':
		open = isTrue(request.form['open'])
		return submitStatus(open)
	elif request.method == 'GET':
		return jsonify(getStatus())

"""
Get room archive.
"""
@app.route('/api/room_archive', methods=['GET'])
@crossdomain(origin='*')
def api_room_archive():
	return send_file(ROOM_ARCHIVE_FILE, mimetype='application/json')

"""
Get room status information as image.
"""
@app.route('/api/room_image.png', methods=['GET'])
@app.route('/api/room_image', methods=['GET'])
@crossdomain(origin='*')
def api_room_image():
	filename = OPEN_IMAGE if isRoomOpen() else CLOSED_IMAGE
	return send_file(filename, mimetype="image/png")

"""
Get general information + room status.
"""
@app.route('/api/room_extended')
@app.route('/api/info')
@crossdomain(origin='*')
def api_info():
	return jsonify(info())
