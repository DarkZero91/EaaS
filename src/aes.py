#!/usr/bin/env python

from Crypto.Cipher import AES
from Crypto import Random
import uuid

from src.keymanager import KeyManager

class AESHelper:
	keymanager = KeyManager()

	@staticmethod
	def get_encrypted_content(content):
		identifier = uuid.uuid4().hex
		key = AESHelper.keymanager.generate_key()
		AESHelper.keymanager.store_key(identifier, key)
		return AESHelper._encrypt(content, key, identifier)
	
	@staticmethod
	def get_decrypted_content(content):
		identifier = content[0:32]
		key = AESHelper.keymanager.load_key(identifier)
		return AESHelper._decrypt(content[32:], key)

	@staticmethod	
	def _encrypt(content, key, identifier):
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(key, AES.MODE_CFB, iv)
		return identifier + iv + cipher.encrypt(content)
	
	@staticmethod
	def _decrypt(content, key):
		cipher = AES.new(key, AES.MODE_CFB, content[0:16])
		return cipher.decrypt(content[16:])
