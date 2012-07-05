#!/usr/bin/python

import sys
import os
from restkit import Resource, BasicAuth, Connection, request
from socketpool import ConnectionPool
import json

def usage():
    print "%s: <github username> <github password>" % sys.argv[0]

if not len(sys.argv) == 3:
    usage()
    exit()

username = sys.argv[1]
password = sys.argv[2]

"""
Authorization/use of the V3 Github API is taken from the code snippet at:
    http://agrimmsreality.blogspot.com/2012/05/sampling-github-api-v3-in-python.html
"""

pool = ConnectionPool(factory=Connection)
API_URL = "https://api.github.com"

auth=BasicAuth(username, password)
authreqdata = {"scopes": ["public_repo"], "note": "admin script"}

resource = Resource('https://api.github.com/authorizations', 
        pool=pool,
        filters=[auth])
response = resource.post(headers={"Content-Type": "application/json"},
        payload=json.dumps(authreqdata))
token = json.loads(response.body_string())['token']

"""
Test to make sure the token works.
"""

resource = Resource('https://api.github.com/%s/repos' % username, pool=pool)
headers = {'Content-Type' : 'application/json',
           'Authorization' : 'token %s' % token } 
response = resource.get(headers = headers)
repos = json.loads(response.body_string())
if not repos:
    print 'Could not get a token for %s from github!' % username
    exit(1)

with open('github_authtoken.json','w') as fh:
    fh.write(json.dumps(token))

