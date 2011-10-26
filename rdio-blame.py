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

response = client.request('http://api.rdio.com/1/', 'POST',
  urllib.urlencode({'method': 'getHeavyRotation', 'user': user, 'friends': 1,  'extras': '-trackKeys', 'limit': 12}))
hr = json.loads(response[1])['result']

for album in hr:
  print "%s - %s" %( album['artist'], album['name'] )
  print "\t Score: %s" % (album['hits'])
