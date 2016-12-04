# import psycopg2
import sqlite3
import os
import time
import getopt
import logging

class Borg:
	_shared_state = {}
	def __init__(self):
		self.__dict__ = self._shared_state

class Configuration(Borg):
	def __init__(self):
		Borg.__init__(self)
		self.dbUsername = os.getenv('DB_USERNAME', "postgres")
		self.dbPassword = os.getenv('DB_PASSWORD', "dionysus")
		self.dbName = os.getenv('DB_NAME', "uranusdb")
		self.dbHost = os.getenv('DB_HOST', 'localhost')

	def getDatabaseConnection(self):
		try:
			return sqlite3.connect('/var/lib/dionysus/sensors.db')
		except:
			logging.error("Unable to connecto to sqlite.")
			raise
