#!/usr/bin/env python

import json
from src.plugins.plugin import Plugin

class Dropbox(Plugin):
	@staticmethod
	def get_user_identifier(accesstoken):
		response = Dropbox._api_call(
				"api.dropbox.com",
				"/1/account/info",
				"GET",
				{"Authorization": "Bearer " + accesstoken}
			)
		data = response.read()
		js = json.loads(data)
		return js['uid']
