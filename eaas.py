#!/usr/bin/env python

import os
import re
from libmproxy import proxy, flow
from Crypto.Cipher import AES
from Crypto import Random

class EaaS(flow.FlowMaster):
	key = "0123456789ABCDEF"

	def run(self):
		try:
			flow.FlowMaster.run(self)
		except:
			self.shutdown()

	def handle_request(self, r):
		f = flow.FlowMaster.handle_request(self, r)
		if f:
			print "Request: %s:%d %s" %(r.host, r.port, r.path)

			# /files_put
			if(r.host == "api-content.dropbox.com" and r.path.startswith("/1/files_put/")):
				try:
					r.content = self._encrypt(r.content)
				except	Exception as e:
					print e

			r.reply()
		return f

	def handle_response(self, r):
		f = flow.FlowMaster.handle_response(self, r)
		if f:
			print "Response for: %s:%d %s" %(r.request.host, r.request.port, r.request.path)

			# /files (GET)
			if(r.request.host == "api-content.dropbox.com" and r.request.path.startswith("/1/files/")):				
				try:
					#print "Content-Encoding: " + r.headers.get_first("content-encoding")
					r.content = self._decrypt(r.content)
				except	Exception as e:
					print e

			r.reply()
		return f
	
	def _encrypt(self, content):
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(EaaS.key, AES.MODE_CFB, iv);
		return iv + cipher.encrypt(content)
	
	def _decrypt(self, content):
		cipher = AES.new(EaaS.key, AES.MODE_CFB, content[0:16]);
		return cipher.decrypt(content[16:])
		

config = proxy.ProxyConfig(
	cacert = os.path.expanduser("~/.mitmproxy/mitmproxy-ca.pem")
)
state = flow.State()
server = proxy.ProxyServer(config, 8080)
m = EaaS(server, state)
m.run()
