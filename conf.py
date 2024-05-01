import os

# timeout per request in seconds (adjust WSGI/proxy timeout settings)
REQUEST_TIMEOUT = 120

# path to REST API files
API_PATH = os.path.abspath(os.path.dirname(__file__))

# access tuples
API_ACCESS = [ ("api-user", "APIKEY") ]

# file to save room status in
ROOM_STATUS_FILE = "%s/data/room.json" % API_PATH

# file to save room archive in
ROOM_ARCHIVE_FILE = "%s/data/archive.json" % API_PATH

# image location
OPEN_IMAGE = "%s/data/open.png" % API_PATH
CLOSED_IMAGE = "%s/data/closed.png" % API_PATH
