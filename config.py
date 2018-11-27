"""
Constants for jim-protocol, settings
"""

# Keys
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
RESPONSE = 'response'
ERROR = 'error'
TO = 'to'
FROM = 'from'
MESSAGE = 'message'

# Values
PRESENSE = 'presence'  # service message for notifying the server about the presence of a client online
MSG = 'msg'  # simple message to the user or chat

# Response codes from server
BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400
SERVER_ERROR = 500
