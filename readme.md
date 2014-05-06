Encryption as a Service
=====================

**What it is:**

The encryption as a service proxy encrypts/decrypts the payload of http(s) requests and responses
based on the url of the host. This enables data to be encrypted before they are stored in
the cloud.

**Setup:**

* make sure you have Python 2.7.x. installed.
* [install pip](http://pip.readthedocs.org/en/latest/installing.html) for automatically installing dependencies.
* run `pip install -r requirements.txt`
* run `python eaas.py`

**requirements:**

* [Python](https://www.python.org/) 2.7.x.
* [pip](http://www.pip-installer.org)
* [mitmproxy](http://mitmproxy.org/)
