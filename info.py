from .room import isRoomOpen, getStatus
from .conf import *

def info():
	roomIsOpen = isRoomOpen()

	message = {
		'api': '0.13',
		'space': 'Freies Labor',
		'url': 'https://freieslabor.org',
		'icon': {
			'open': 'https://blog.freieslabor.org/images/open.png',
			'closed': 'https://blog.freieslabor.org/images/closed.png'
		},
		'location': {
			'address': 'Richthofenstr. 29, 31137 Hildesheim, Germany',
			'lat': 52.168625,
			'lon': 9.947232,
		},
		'contact': {
			'email': 'kontakt@freieslabor.org',
			'ml': 'freieslabor@freieslabor.org'
		},
		'logo': 'https://blog.freieslabor.org/images/logo.svg',
		'state': {
			'open': roomIsOpen,
			'lastchange': getStatus()['since'],
			'message': infoMessage(roomIsOpen),
			'icon': {
				'open': 'https://blog.freieslabor.org/images/open.png',
				'closed': 'https://blog.freieslabor.org/images/closed.png'
			}
		},
		'issue_report_channels': [
			'email'
		],
		'projects': [ 'http://github.com/freieslabor' ]
	}
	return message

def infoMessage(roomIsOpen):
	return 'Open for public!' if roomIsOpen else 'We\'re closed.'
