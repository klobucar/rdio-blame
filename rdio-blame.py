#!/usr/bin/env python

import sys
import json
import oauth2 as oauth
import urllib
from collections import defaultdict

RDIO_CONSUMER_KEY = ''
RDIO_CONSUMER_SECRET = ''

if len(sys.argv) > 1:
  username = sys.argv[1]
else:
	username = getpass.getuser()

consumer = oauth.Consumer(RDIO_CONSUMER_KEY, RDIO_CONSUMER_SECRET)
client = oauth.Client(consumer)

def name(u):
  return u['firstName'] + " " + u['lastName']

def hr(user):
  response = client.request('http://api.rdio.com/1/', 'POST',
    urllib.urlencode({'method': 'getHeavyRotation', 'user': user, 'friends': 1,  'extras': '-trackKeys', 'limit': 12}))
  return json.loads(response[1])['result']

def userFromVanity(name):
  user_response = client.request('http://api.rdio.com/1/', 'POST',
    urllib.urlencode({'method': 'findUser', 'vanityName': name }))
  return json.loads(user_response[1])['result']

currentUser = userFromVanity(username)

follows_response = client.request('http://api.rdio.com/1/', 'POST',
  urllib.urlencode({'method': 'userFollowing', 'user': currentUser['key']}))

follows = json.loads(follows_response[1])['result']

friends = {}
albums = defaultdict(list)

print "\nHeavy Rotation for %s\n" % unicode(currentUser['firstName'] + " " + currentUser['lastName'])

sys.stdout.write("Loading")
sys.stdout.flush()

for friend in follows:
  friends[friend['key']] = friend
  sys.stdout.write(".")
  sys.stdout.flush()
  for album in hr(friend['key']):
    albums[album['key']].append(friend['key'])

print ""

for album in hr(currentUser['key']):
  print " %s - %s" %( album['artist'], album['name'] )
  for friendKey in albums[album['key']]:
    print "   "+name(friends[friendKey])
  print ""
