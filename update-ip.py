#!/usr/bin/env python

import xmlrpclib
import urllib2
import sys

zone_name = 'eightbits'
api = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')
api_key = 'XXXXX'
api_version = api.version.info(api_key)

ip_address = urllib2.urlopen('http://icanhazip.com').read()
print >> sys.stderr, "current ip=%s" % (ip_address)

zone_id = [ z['id'] for z in api.domain.zone.list(api_key) if z['name'] == zone_name]
zone_id = zone_id.pop()

print >> sys.stderr, "zone id = %s" % zone_id

zone_version = api.domain.zone.version.new(api_key, zone_id)

print >> sys.stderr, "zone version = %s" % zone_version

print >> sys.stderr, api.domain.zone.record.delete(
        api_key,
        zone_id,
        zone_version,
        { "type": "A", "name": "snowcrash" }
)

print >> sys.stderr, api.domain.zone.record.add(
        api_key,
        zone_id,
        zone_version,
        { "type": "A", "name": "snowcrash", "ttl": 300, "value": ip_address }
)

print >> sys.stderr, api.domain.zone.version.set(
    api_key,
    zone_id,
    zone_version
)
