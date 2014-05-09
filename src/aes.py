#!/usr/bin/env python

from Crypto.Cipher import AES
from Crypto import Random
import uuid

import src.keymanager

class AESHelper(object):
	
	def __init__(self):
		self.keymanager = src.keymanager.KeyManager()

	def get_encrypted_content(self, host, content, token, label):
		key = self.keymanager.get_key(host, token, label)
		return AESHelper._encrypt(content, key)
	
	def get_decrypted_content(self, host, content, token, label):
		key = self.keymanager.get_key(host, token, label)
		return AESHelper._decrypt(content, key)

	@staticmethod
	def _encrypt(content, key):
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(key, AES.MODE_CFB, iv)
		return iv + cipher.encrypt(content)
	
	@staticmethod
	def _decrypt(content, key):
		cipher = AES.new(key, AES.MODE_CFB, content[0:16])
		return cipher.decrypt(content[16:])
