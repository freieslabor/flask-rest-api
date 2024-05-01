import os

# timeout per request in seconds (adjust WSGI/proxy timeout settings)
REQUEST_TIMEOUT = 120

# path to REST API files
API_PATH = os.path.abspath(os.path.dirname(__file__))

# access tuples
API_ACCESS = [ ("api-user", "APIKEY") ]

# file to save room status in
ROOM_STATUS_FILE = "%s/data/room.json" % API_PATH


