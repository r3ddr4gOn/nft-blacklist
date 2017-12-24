#!/usr/bin/env python3

# Python script for updating the nftables blacklist

import urllib.request

# Variables (Change accordingly)
ip_file = '/etc/nftables/inet_filter_ip_black_country.inc'
ip6_file = '/etc/nftables/inet_filter_ip6_black_country.inc'
# ISO 3166 ALPHA2 country codes
country_codes = ('cn', 'ru')

# Constants
FILE_HEADER = 'elements = {'
FILE_FOOTER = '}'
IPDENY_IP_URL = 'http://www.ipdeny.com/ipblocks/data/aggregated/{}-aggregated.zone'
IPDENY_IP6_URL = 'http://www.ipdeny.com/ipv6/ipaddresses/aggregated/{}-aggregated.zone'


def update_blacklist(set_file, url):
    blacklist = []

    # download all requested country ip blocks
    for c in country_codes:
        print('Downloading "{}" IP blocks..'.format(c))
        ip_blocks = urllib.request.urlopen(url.format(c))
        data = ip_blocks.read().decode('utf-8')
        blacklist.extend(data.splitlines())

    # concatenate all ip blocks
    blacklist = ',\n'.join(blacklist)

    print('Updating the blacklist file..')
    with open(set_file, 'w') as f:
        f.write('\n'.join((FILE_HEADER, blacklist, FILE_FOOTER, '')))


def update_blacklists():
    if ip_file:
        update_blacklist(ip_file, IPDENY_IP_URL)
    if ip6_file:
        update_blacklist(ip6_file, IPDENY_IP6_URL)
    print('Done!')


if __name__ == '__main__':
    update_blacklists()
