# For domains that use GANDI.net DNS
# Updates a DNS A record with a current public IP address

- uses gandi API to get zone information
- uses icanhazip.com to get a current public IP address
- work in progress

Example of the config file:

  [client]
  key = <api-key>
  zone_name = <gandi-zone-name>
  domain_name = <domain-name-to-update>
  ttl = <time-to-live-for-a-dns-record-in-seconds>
