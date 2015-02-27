#!/usr/bin/env python

import json
import time
import pytumblr

with open('credentials.json') as f:
  data = json.load(f)

client = pytumblr.TumblrRestClient(
  data["consumer_key"],
  data["consumer_secret"],
  data["oauth_token"],
  data["oauth_token_secret"]
)

name      = client.info()['user']['name']
num_likes = client.info()['user']['likes']
processed = 0

print "[INFO] username: %s, liked posts: %d" % (name, num_likes)

done = 0
ts = []
# TODO write the seen_ids out to a file
seen_ids = set() 

while done != 1:
  if processed == 0:
    likes = client.likes(limit=49)
  else:
    likes = client.likes(limit=49, before=ts_before)

  # uncomment next line if you want the raw json
  #print likes

  for l in likes['liked_posts']:
    if l['id'] not in seen_ids:
      seen_ids.add(l['id'])
      ts.append(l['timestamp'])
      try: 
        for p in l['photos']:
          print p['original_size']['url']
      except KeyError:
        pass # liked post didn't contain a photo
    else:
      pass

  processed = processed + len(ts)

  if len(ts) > 0:
    # we will get dupes, but we need to catch these...
    ts_before = min(ts) + 10 
  else:
    # we are out of things to process...
    # it's possible that the number of processed != number of liked
    # probably because tumblr doesn't update the number of liked posts
    # when a user's tumblr no longer exists for some reason
    print "[INFO] processed %d, we had %d liked" % (processed, num_likes)
    done = 1

  print "[INFO] processed %d liked posts, now requesting liked posts with ts < %s" % (processed, str(ts_before))

  ts = []
  time.sleep(0.5) # let's try not to hammer their servers
