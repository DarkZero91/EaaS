#!/usr/bin/env python

from Crypto import Random

class KeyManager(object):
	master_key = "0123456789ABCDEF"
	
	def generate_key(self):
		return KeyManager.master_key #Random.new().read(32)

	def store_key(self, uuid, key):
		pass
		
	def load_key(self, uuid):
		return KeyManager.master_key

	def delete_key(self, uuid):
		pass
