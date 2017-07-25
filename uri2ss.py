#!/usr/bin/env python3

import base64
import collections
import json
import re
import sys


def decode_unpaded_base64(s):
    try:
        return base64.b64decode(s + '=' * (-len(s) % 4)).decode('utf-8', 'replace')
    except Exception:
        return ''


def match_uri(uri):
    # IPv6 plain
    match = re.match(r'ss://([^:@]*?):(.*)@\[([^]@]*?)\]:(\d+)(?:#(.*))?$', uri)
    if match is not None:
        return match.groups()
    # IPv4 plain
    match = re.match(r'ss://([^:@]*?):(.*)@([^:@]*?):(\d+)(?:#(.*))?$', uri)
    if match is not None:
        return match.groups()
    # base64 password, IPv6 plain
    match = re.match(r'ss://[A-Za-z0-9+/=]*@\[([^]@]*?)\]:(\d+)(?:#(.*))?$', uri)
    if match is not None:
        method_password, server, server_port, remarks = match.groups()
        match = re.match(r'(.*?):(.*)$', method_password)
        if match is not None:
            method, password = match.groups()
            return method, password, server, server_port, remarks
    # base64 password, IPv4 plain
    match = re.match(r'ss://[A-Za-z0-9+/=]*@([^:@]*?):(\d+)(?:#(.*))?$', uri)
    if match is not None:
        method_password, server, server_port, remarks = match.groups()
        method_password = decode_unpaded_base64(method_password)
        match = re.match(r'(.*?):(.*)$', method_password)
        if match is not None:
            method, password = match.groups()
            return method, password, server, server_port, remarks
    # base64 encoded
    match = re.match(r'ss://([A-Za-z0-9+/=]*)(?:#(.*))?$', uri)
    if match is not None:
        uri_main, remarks = match.groups()
        uri_main = decode_unpaded_base64(uri_main)
        # IPv6 base64
        match = re.match(r'([^:@]*?):(.*)@\[([^]@]*?)\]:(\d+)$', uri_main)
        if match is not None:
            method, password, server, server_port = match.groups()
            return method, password, server, server_port, remarks
        # IPv4 base64
        match = re.match(r'([^:@]*?):(.*)@([^:@]*?):(\d+)$', uri_main)
        if match is not None:
            method, password, server, server_port = match.groups()
            return method, password, server, server_port, remarks
    raise ValueError('Invalid URI: {!r}'.format(uri))

def uri2ss(uri):
    uri = uri.strip()
    method, password, server, server_port, remarks = match_uri(uri)
    conf = collections.OrderedDict([
        ('server', server),
        ('server_port', server_port),
        ('local_address', '127.0.0.1'),
        ('local_port', 1080),
        ('password', password),
        ('method', method),
        ('mode', 'tcp_and_udp'),
        ('ipv6_first', True),
    ])
    if method.endswith('-auth'):
        conf['method'] = method[:-5]
        conf['auth'] = True
    if remarks:
        conf['remarks'] = remarks
    return conf


def main(argv):
    if len(argv) == 1:
        for line in sys.stdin:
            conf = uri2ss(line)
            json.dump(conf, sys.stdout, indent=4)
            sys.stdout.write('\n\n')
    else:
        for i in argv[1:]:
            conf = uri2ss(i)
            json.dump(conf, sys.stdout, indent=4)
            sys.stdout.write('\n\n')

if __name__ == '__main__':
    main(sys.argv)
