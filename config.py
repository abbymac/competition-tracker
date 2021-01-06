import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgres://wiegupgmizfcym:555d35f3e5cd08525dc2109428d4f9ff0a60f37d21aa57e7b3a9926820b6d92b@ec2-54-156-73-147.compute-1.amazonaws.com:5432/d1vqqjqkf74gna'
# SQLALCHEMY_DATABASE_URI = 'postgresql://abbymac@localhost:5432/capstone'