#!/usr/bin/env python

import redis

r = redis.Redis(host='localhost', port=6379, db=0)
print("r = redis")

r.set('foo', 'bar')
print ("foo=bar")
