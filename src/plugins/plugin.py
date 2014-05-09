#!/usr/bin/env python

import httplib

class Plugin(object):
	@staticmethod
	def _api_call(host, path, method, headers):
		connection = httplib.HTTPSConnection(host)
		connection.request(method, path, "", headers)
		return connection.getresponse()
		
		
