#!/usr/bin/env python

import xmlrpclib
import urllib2
import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/etc/gandi-api-key')
api_key = config.get('client', 'key')
zone_name =  config.get('client', 'zone_name')
domain_name = config.get('client', 'domain_name')
ttl = config.getint('client', 'ttl')

api = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')
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
        { "type": "A", "name": domain_name }
)

print >> sys.stderr, api.domain.zone.record.add(
        api_key,
        zone_id,
        zone_version,
        { "type": "A", "name": domain_name, "ttl": ttl, "value": ip_address }
)

print >> sys.stderr, api.domain.zone.version.set(
    api_key,
    zone_id,
    zone_version
)
