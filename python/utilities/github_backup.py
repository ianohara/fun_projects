#!/usr/bin/python

import sys
import os
from restkit import Resource, BasicAuth, Connection, request
from socketpool import ConnectionPool
import json

def usage():
    print "%s: <github username> <backup directory>" % sys.argv[0]

if not len(sys.argv) == 4:
    usage()
    exit()

username = sys.argv[1]
password = sys.argv[2]
backup_dir = sys.argv[3]

os.chdir(backup_dir)

"""
Authorization/use of the V3 Github API is taken from the code snippet at:
    http://agrimmsreality.blogspot.com/2012/05/sampling-github-api-v3-in-python.html
"""

pool = ConnectionPool(factory=Connection)

with open('github_authtoken.json', 'r') as f:
    token = json.loads(f.read())

resource = Resource('https://api.github.com/%s/repos' % username, pool=pool)
headers = {'Content-Type' : 'application/json',
           'Authorization' : 'token %s' % token } 
response = resource.get(headers = headers)
decoded = json.loads(response.body_string())

if not decoded:
    print 'Could not get repos for %s from github!' % username
    exit(1)

repo_urls = list()
repo_names = list()

for proj in decoded['repositories']:
    name = proj['name']
    url = proj['url']
    repo_urls.append(url)
    repo_names.append(name)
    if not os.path.isdir(name):
        print "Cloning repo %s at %s" % (name, url)
        os.system("git clone %s" % url)
    else:
        tmp_dir = os.curdir
        os.chdir(name)
        print "Pulling repo %s at %s" % (name, url)
        os.system("git pull")
        os.chdir('..')
