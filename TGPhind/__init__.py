from __future__ import annotations

from dataclasses import dataclass
from http.client import HTTPResponse
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from string import punctuation
from typing import Iterator
from urllib.error import URLError
from urllib.request import Request, urlopen

from TGPhind.Parser import *

__all__ = ('TRANSCRIPT', 'TGPhind', 'MIRRORS', 'Proxy')

TRANSCRIPT = str.maketrans(
    {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'eh', 'ю': 'yu', 'я': 'ya', ' ': '-'
    } | {i: '' for i in punctuation.replace(' ', '')})

MONTH = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
MIRRORS = ['te.legra.ph', 'graph.org', 'telegra.ph']


@dataclass
class Proxy:
    host: str = ''
    protocol: str = 'https'

    def __bool__(self) -> bool:
        return bool(self.host and self.protocol)


class TGPhind:
    def __init__(self, MAX_TH: int = None,
                 proxy: Proxy = None,
                 brackets='<>'):
        self.MAX_TH = MAX_TH or cpu_count()
        self.proxy = Proxy() if proxy is None else proxy
        self.brackets = brackets

    def search(self, template: str) -> tuple[str] | tuple:
        return self.search_iter(parse(template, self.brackets))

    def search_iter(self, names: Iterator[str]) -> tuple[str] | tuple:
        self.__result = ()
        args = ()
        names = (*(name.lower().translate(TRANSCRIPT) for name in names),)
        for m in range(1, 13):
            for d in range(1, MONTH[m - 1] + 1):
                for name in names:
                    args += (name, m, d),
        with ThreadPool(self.MAX_TH) as pool:
            pool.starmap(self.__handle, args)
        return *sorted(self.__result),

    def test_mirrors(self):
        for host in MIRRORS:
            try:
                self.urlopen('', host)
            except URLError:
                MIRRORS.remove(host)

    def __handle(self, name: str, m: int, d: int, n: int = 0):
        path = f'{name}-{m:0>2}-{d:0>2}'
        if n:
            path += f'-{n}'
        try:
            self.urlopen(path)
            self.__result += path,
            if not n:
                n = 2
            else:
                n += 1
        except URLError:
            return
        self.__handle(name, m, d, n)

    def urlopen(self, path: str, host=None) -> HTTPResponse:
        if not host:
            host = MIRRORS[0]
        proxy = self.proxy
        protocol = proxy.protocol
        req = Request(join(protocol, host, path), headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/102.0.0.0 Safari/537.36'})
        if proxy:
            req.set_proxy(proxy.host, protocol)
        return urlopen(req, timeout=5.)

    def map_hosts(self, results: tuple[str] = (), protocol: str = None, test_mirrors: bool = True) -> tuple[tuple[str]]:
        if test_mirrors:
            self.test_mirrors()
        if not protocol:
            protocol = self.proxy.protocol
        return *((*(join(protocol, host, name) for host in MIRRORS),) for name in results),
