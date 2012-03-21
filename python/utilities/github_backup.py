#!/usr/bin/python

import sys
import os
import urllib
import json

def usage():
    print "%s: <github username> <backup directory>" % sys.argv[0]

if not len(sys.argv) is 3:
    usage()
    exit()

username = sys.argv[1]
backup_dir = sys.argv[2]

os.chdir(backup_dir)

url_fh = urllib.urlopen("http://github.com/api/v2/json/repos/show/%s" % username)

decoded = json.load(url_fh)

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
