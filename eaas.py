#!/usr/bin/env python

import os
import re

from libmproxy import proxy, flow
import src.aes

class EaaS(flow.FlowMaster):

	def run(self):
		self.aes = src.aes.AESHelper()

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
					token = r.headers['Authorization'][0].split(" ")[1]
					label = re.search("/1/files_put/sandbox/(.*\.md)", r.path)

					r.content = self.aes.get_encrypted_content("Dropbox", r.content, token, label.group(1))
				except	Exception as e:
					print "Exception: " + str(e)

			r.reply()
		return f

	def handle_response(self, r):
		f = flow.FlowMaster.handle_response(self, r)
		if f:
			print "Response for: %s:%d %s" %(r.request.host, r.request.port, r.request.path)

			# /files (GET)
			if(r.request.host == "api-content.dropbox.com" and r.request.path.startswith("/1/files/")):				
				try:
					token = r.request.headers['Authorization'][0].split(" ")[1]
					label = re.search("/1/files/sandbox/(.*\.md)", r.request.path)
					#print "Content-Encoding: " + r.headers.get_first("content-encoding")

					r.content = self.aes.get_decrypted_content("Dropbox", r.content, token, label.group(1))
				except	Exception as e:
					print "Exception: " + str(e)

			r.reply()
		return f		

config = proxy.ProxyConfig(
	cacert = os.path.expanduser("~/.mitmproxy/mitmproxy-ca.pem")
)
state = flow.State()
server = proxy.ProxyServer(config, 8080)
m = EaaS(server, state)
m.run()
