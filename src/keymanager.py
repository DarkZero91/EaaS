#!/usr/bin/env python

from Crypto import Random
import pickle
import os.path
import os

import src.aes
from src.plugins.dropbox import Dropbox

class KeyManager(object):
	def __init__(self):
		self.master_key = "0123456789ABCDEF"
		self.identifiers = {} # {host: {token: identifier}}
		self.keys = {} # {host: {token: {label: key}}}

		if not os.path.isdir("keys"):
			os.mkdir("keys")
	
	# Key operations

	def get_key(self, host, token, label):
		if not host in self.keys:
			self.keys[host] = {}

		if token in self.keys[host]:
			if label in self.keys[host][token]:
				return src.aes.AESHelper._decrypt(self.keys[host][token][label], self.master_key)
			else:
				key = self._generate_key()
				self.keys[host][token][label] = src.aes.AESHelper._encrypt(key, self.master_key)
				self._store_keys(host, token)
				return key
		else:
			self._load_keys(host, token)
			return self.get_key(host, token, label)

	def delete_key(self, host, token, label):
		del self.keys[host][token][label]
		if len(self.keys[host][token]) == 0:
			keystore = "keys/" + host + "/" + self._get_identifier(host, token) + ".keys"
			del self.keys[host][token]
			os.remove()
	
	# helpers

	def _load_keys(self, host, token):
		keystore = "keys/" + host + "/" + self._get_identifier(host, token) + ".keys"
		
		if os.path.isfile(keystore):
			f = open(keystore, 'rb+')
			self.keys[host][token] = pickle.load(f)
			f.close()
		else:
			if not os.path.isdir("keys/" + host):
				os.mkdir("keys/" + host)
			
			f = open(keystore, 'wb+')
			f.close()
			self.keys[host][token] = {}

	def _store_keys(self, host, token):
		keystore = "keys/" + host + "/" + self._get_identifier(host, token) + ".keys"

		f = open(keystore, 'wb+')
		pickle.dump(self.keys[host][token], f)
		f.close()

	def _generate_key(self):
		return Random.new().read(32)

	def _get_identifier(self, host, token):
		if not host in self.identifiers:
			self.identifiers[host] = {}		

		if not token in self.identifiers[host]:
			self.identifiers[host][token] = Dropbox.get_user_identifier(token)

		return str(self.identifiers[host][token])
	
