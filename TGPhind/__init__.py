from dataclasses import dataclass
from http.client import HTTPResponse
from multiprocessing import cpu_count
from string import punctuation
from threading import Thread
from typing import Any, Iterator, Union
from urllib.error import URLError
from urllib.request import Request, urlopen

from .Parser import *

__all__ = ('TRANSCRIPT', 'TGPhind', 'MIRRORS', 'set_mirrors', 'set_brackets', 'Proxy')

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

MONTH = 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31


@dataclass
class Proxy:
    host: str = ''
    protocol: str = 'https'

    def __bool__(self) -> bool:
        return bool(self.host and self.protocol)


MIRRORS = ['te.legra.ph', 'graph.org', 'telegra.ph']


def set_mirrors(to):
    global MIRRORS
    MIRRORS = [str(i) for i in to]


class TGPhind:
    def __init__(self, article_name: str,
                 MAX_TH: Any = cpu_count(),
                 proxy: Proxy = Proxy(),
                 BRACKETS='<>'):
        self.article_name = article_name
        self.MAX_TH = MAX_TH
        self.proxy = proxy
        set_brackets(BRACKETS)

    @property
    def result(self) -> Union[tuple[str], tuple]:
        if not hasattr(self, '__result'):
            self.start(parse(self.article_name))
        return self.__result

    def only_paths(self) -> tuple[str]:
        return self.result

    def hosts_map(self, mirrors=None) -> tuple[tuple[str]]:
        if mirrors is None:
            mirrors = MIRRORS
        protocol = self.proxy.protocol
        return tuple(tuple(join(protocol, host, path) for host in mirrors) for path in self.result)

    def start(self, names: Iterator[str]):
        self.__result = ()
        names = tuple(name.lower().translate(TRANSCRIPT) for name in names)
        threads = ()
        MAX_TH = self.MAX_TH
        for m in range(1, 13):
            for d in range(1, MONTH[m - 1] + 1):
                for name in names:
                    th = Thread(target=self.__handle, args=(name, m, d))
                    th.start()
                    threads += th,
                    if len(threads) == MAX_TH:
                        for th in threads:
                            th.join()
                        threads = ()
        for th in threads:
            th.join()

    def test_mirrors(self):
        for host in MIRRORS:
            try:
                self.urlopen('', host)
            except URLError:
                MIRRORS.remove(host)

    def __handle(self, name: str, m: int, d: int, n: int = 0):
        path = f'{name}-{m}-{d}'
        if n:
            path += f'-{n}'
            n += 1
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
        req = Request(join(protocol, host, path))
        if proxy:
            req.set_proxy(proxy.host, protocol)
        return urlopen(req, timeout=2.5)
