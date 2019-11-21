import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

# Twilio keys
account_sid = ''
auth_token = ''
from_phone = '+15005550006'

# sendgrid key
SENDGRID_API_KEY = ''

#Office Address
address = '4560 1 Javier Street, Dallas, Texas'