#!/usr/bin/env python3

import base64
import json
import sys
import urllib.parse


def ss2uri(conf):
    method = conf.get('method', 'table')
    assert ':' not in method
    server = conf.get('server', '0.0.0.0')
    if ':' in server:
        server = '[' + server + ']'
    server_port = str(conf.get('server_port', '8388'))
    password = conf.get('password', '')
    if conf.get('auth', False):
        method += '-auth'
    plain = '{}:{}@{}:{}'.format(method, password, server, server_port)
    encoded = base64.b64encode(plain.encode('utf-8', 'replace')).rstrip(b'=').decode('utf-8', 'replace')
    remarks = conf.get('remarks', '')
    if remarks:
        encoded += '#'
        encoded += urllib.parse.quote(remarks)
    return 'ss://' + encoded


def main(argv):
    if len(argv) == 1:
        print('Usage: {} config.json'.format(argv[0]))
        print()
    for i in argv[1:]:
        with open(i, 'r', encoding='utf-8', errors='replace') as f:
            conf = dict(json.load(f))
            print(ss2uri(conf))


if __name__ == '__main__':
    main(sys.argv)
