#!/usr/bin/env python

import sys
import json
import oauth2 as oauth
import urllib

RDIO_CONSUMER_KEY = '<CONSUMER_KEY>'
RDIO_CONSUMER_SECRET = '<CONSUMER_SECRET>'

if sys.argv[1][0] is not "s":
  user = "s" + sys.argv[1]
else:
  user = sys.argv[1]

consumer = oauth.Consumer(RDIO_CONSUMER_KEY, RDIO_CONSUMER_SECRET)
client = oauth.Client(consumer)
response = client.request('http://api.rdio.com/1/', 'POST', 
  urllib.urlencode({'method': 'getHeavyRotation', 'user': user, 'friends': 1,  'extras': '-trackKeys', 'limit': 12}))
hr = json.loads(response[1])['result']

for album in hr:
  print "%s - %s" %( album['artist'], album['name'] )

