#!/usr/bin/env python

import sys
import json
import oauth2 as oauth
import urllib
import getpass

RDIO_CONSUMER_KEY = ''
RDIO_CONSUMER_SECRET = ''

if len(sys.argv) > 1:
  username = sys.argv[1]
else:
  username = getpass.getuser()

consumer = oauth.Consumer(RDIO_CONSUMER_KEY, RDIO_CONSUMER_SECRET)
client = oauth.Client(consumer)

user_response = client.request('http://api.rdio.com/1/', 'POST',
  urllib.urlencode({'method': 'findUser', 'vanityName': username }))

currentUser = json.loads(user_response[1])['result']

print "\nHeavy Rotation for %s\n" % unicode(currentUser['firstName'] + " " +  currentUser['lastName'])

response = client.request('http://api.rdio.com/1/', 'POST',
  urllib.urlencode({'method': 'getHeavyRotation', 'user': currentUser['key'], 'friends': 1,  'extras': '-trackKeys, users', 'limit': 12}))
hr = json.loads(response[1])['result']

for album in hr:
  print "  %s - %s" %( album['artist'], album['name'] )
  for user in album['users']:
    print "\t Name: %s URL: http://rdio.com%s " % ( unicode(user['firstName'] + " " +  user['lastName']).ljust(20), user['url'])
  print ""
