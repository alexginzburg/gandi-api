#!/usr/bin/env python
'''
    gandi api to update an ip address
'''

import xmlrpclib
import urllib2
import sys
import ConfigParser

def main():
    '''
        gandi api to update an ip address
    '''

    config = ConfigParser.ConfigParser()
    config.read('/etc/gandi-api-key')
    api_key = config.get('general', 'key')
    zone_name = config.get('general', 'zone_name')
    ttl = config.getint('general', 'ttl')

    domains_to_update = [v for _, v in config.items('domain')]

    _update_domain(api_key, zone_name, domains_to_update, ttl)

def _create_api_client(api_key):
    '''
        gandi api to update an ip address
    '''

    api = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')
    _ = api.version.info(api_key)
    return api

def _get_current_address():
    '''
        gandi api to update an ip address
    '''
    return urllib2.urlopen('http://icanhazip.com').read()

def _get_zone_for_name(api, api_key, zone_name):
    '''
        gandi api to update an ip address
    '''

    zone_id = [
                z['id'] for z in api.domain.zone.list(api_key)
                if z['name'] == zone_name
    ]
    return zone_id.pop()

def _update_domain(api_key, zone_name, domain_list, ttl):
    '''
        gandi api to update an ip address
    '''

    api = _create_api_client(api_key)
    zone_id = _get_zone_for_name(api, api_key, zone_name)
    ip_address = _get_current_address()

    zone_version = api.domain.zone.version.new(api_key, zone_id)

    for domain_name in domain_list:
        print >> sys.stderr, "delete %s in version %s with result = %s" % (
                domain_name,
                zone_version,
                api.domain.zone.record.delete(
                    api_key,
                    zone_id,
                    zone_version,
                    {"type": "A", "name": domain_name}
                )
        )

        print >> sys.stderr, "add %s in version %s with result = %s" % (
                domain_name,
                zone_version,
                api.domain.zone.record.add(
                    api_key,
                    zone_id,
                    zone_version,
                    {
                        "type": "A",
                        "name": domain_name,
                        "ttl": ttl,
                        "value": ip_address
                    }
                )
        )

    print >> sys.stderr, "active version %s with result = %s" % (
            zone_version,
            api.domain.zone.version.set(
                api_key,
                zone_id,
                zone_version
            )
    )

if __name__ == '__main__':
    sys.exit(main())
