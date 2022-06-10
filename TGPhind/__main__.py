from __future__ import annotations

import argparse
from urllib.parse import urlparse

import TGPhind


def _proxy_type(arg: str):
    parsed = urlparse(arg)
    return TGPhind.Proxy(parsed.netloc, parsed.scheme or 'https')


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('query', type=str)
    arg_parser.add_argument('-tc', '--threads-count', type=int)
    arg_parser.add_argument('-b', '--brackets', type=str, help='Brackets for templates (Default "<>")', default='<>')
    arg_parser.add_argument('-x', '--proxy', type=_proxy_type, help='protocol://host:port')
    args = arg_parser.parse_args()
    se = TGPhind.TGPhind(args.threads_count, args.proxy, args.brackets)
    se.test_mirrors()
    print(*TGPhind.MIRRORS, sep=', ', end='\n\n')
    print(*se.search(args.query), sep='\n')


if __name__ == '__main__':
    main()
