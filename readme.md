Encryption as a Service
=======================

What it is:
-----------
The encryption as a service proxy encrypts/decrypts the payload of http(s) requests and responses
based on the url of the end point. This enables data to be encrypted before they are stored in
the cloud.

Setup:
------
* [install pip](http://pip.readthedocs.org/en/latest/installing.html) for automatically installing dependencies.
* run `pip install -r requirements.txt`
* run `python eaas.py`

requirements:
-------------
* [Python]() 2.7.x.
* [pip]()
* [mitmproxy]()
