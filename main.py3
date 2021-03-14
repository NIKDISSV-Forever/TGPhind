#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__banner__ = r"""
 _____ ____ ____  _     _           _
|_   _/ ___|  _ \| |__ (_)_ __   __| |
  | || |  _| |_) | '_ \| | '_ \ / _` |
  | || |_| |  __/| | | | | | | | (_| |
  |_| \____|_|   |_| |_|_|_| |_|\__,_|"""
__author__ = "NIKDISSV"
__github__ = "https://github.com/NIKDISSV-Forever/"


from sys import argv
from os import mkdir, remove
from os.path import exists

from typing import Union, List, Tuple, Dict
from re import finditer, findall

from string import punctuation
from time import perf_counter

from threading import Thread
from urllib.request import urlopen, URLError


class TGPhind:

    MM = range(1, 13)
    DD = range(1, 32)

    FOUND_DIR = "found"
    openResult = False

    TOTAL = 0

    @staticmethod
    def try_mirrors(url: str) -> None:
        url = PROTOCOL+url
        try:
            resp = urlopen(url)
        except Exception as Error:
            SITES.remove(url)
            print(url, Error, sep=" : ")
        else:
            print(url, resp.getcode())

    @staticmethod
    def print_preview() -> None:

        from shutil import get_terminal_size
        terminal_size = get_terminal_size()

        for line in __banner__.split("\n"):
            print(line.center(terminal_size.columns, " "))
        print(__author__.center(terminal_size.columns, " "))
        print(__github__.center(terminal_size.columns, " "))
        print()

    @staticmethod
    def argv_Parse() -> None:

        if "-noCls" in argv:
            argv.remove("-noCls")
        else:
            from os import name, system
            system("cls" if name == "nt" else "clear")

        if "-opnRes" in argv:
            TGPhind.openResult = True
            argv.remove("-opnRes")

    @staticmethod
    def Get_Transcript_Dict() -> Dict[str, str]:
        RU_LETTERS = (
            "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я ")
        EN_LETTERS = (
            "a b v g d e yo zh z i j k l m n o p r s t u f h c ch sh shch  y  eh yu ya ")

        PUNCTUATIONS = S.join(punctuation)
        PUNCTUATIONS_L = S*len(punctuation)

        TRANSCRIPT_DICT = dict(zip(
            (RU_LETTERS + PUNCTUATIONS).split(S),
            (EN_LETTERS + PUNCTUATIONS_L).split(S))
        )
        TRANSCRIPT_DICT[S] = "-"

        return TRANSCRIPT_DICT

    @staticmethod
    def Get_Query() -> str:

        while True:
            try:
                query = input("Enter your search term: ").strip().strip(
                    "-").lower()
            except KeyboardInterrupt:
                exit(0)
            except Exception as Error:
                print(Error)
            if query:
                break
            else:
                print("The line is empty!")
        return query

    def __get_on_replace(self, text: str) -> Tuple[str]:

        result = tuple()
        text = text[1:-1].strip()

        fi = tuple(findall(r"(.{1}\-.{1}?)", text))
        for i in fi:
            t = i.split("-")
            result += tuple(map(
                chr,
                range(ord(t[0]), ord(t[-1])+1)
            ))
            text = text.replace(i, "", 1)

        for i in text.split():
            try:
                result += str(eval(i)),
            except:
                result += i,

        return result

    def __template_query(self, query: str) -> Tuple[str]:
        result = fid = tuple()

        fi = tuple(finditer(r"\[(.+?)\]", query))
        query_No_Re = query

        for i in fi:
            span = i.span()
            text = query[span[0]:span[-1]]
            query_No_Re = query_No_Re.replace(text, "")
            fid += (text, self.__get_on_replace(text)),

        result += query_No_Re,

        for i in fid:
            query_No_Re = query
            for j in i[-1]:
                result += query_No_Re.replace(i[0], j),
        result = tuple(sorted(set(result)))

        return result

    def transcript(self,
                   text: str = "",
                   table: Dict[str, str] = None,
                   lowered: bool = True) -> str:

        text = str(text).lower() if lowered else str(text)

        if not table:
            table = self.Get_Transcript_Dict()
        else:
            table = dict(table)

        for i in table:
            if i in text:
                text = text.replace(i, table[i])
        return text

    def Start_Search(self) -> None:

        self.startIn = perf_counter()

        inf = (
            f"Query: {self.query[0]} - Variations: {len(self.query)}",
            f"MM: {self.MM[-1]} DD: {self.DD[-1]}",
            f"Found in: {self.FOUND_DIR}"
        )
        print(*inf, sep=" | ")

        for mm in self.MM:
            for dd in self.DD:
                for query in self.query:
                    mm, dd = str(mm).rjust(2, "0"), str(dd).rjust(2, "0")
                    t = Thread(target=self.Search, args=(mm, dd, query))
                    t.start()

    def Search(self,
               mm: Union[str, int], dd: Union[str, int],
               query: str = None, n: Union[str, int] = "") -> None:

        if not query:
            return

        suf = f"{query}-{mm}-{dd}{n}"
        url = f"{PROTOCOL}{SITES[0]}{suf}"

        try:
            resp = urlopen(url, )
        except Exception as Error:
            if hasattr(Error, "getcode"):
                resp = Error
            else:
                return

        code = resp.getcode()

        if code < 400:
            self.file_handle.write(url+"\n")
            self.TOTAL += 1
            for u in SITES[1:]:
                self.file_handle.write(f"{PROTOCOL}{u}{suf}\n")

            Thread(target=self.Search,
                   args=(mm, dd, query, n-1 if n else -2)
                   ).start()
        print(code, url, sep=" : ")

    def _argParse(self, args: Union[List[str], Tuple[str]] = []) -> list:

        args = list(map(str.lower, args))

        if "-mm" in args:
            try:
                i = args.index("-mm")
                mm = args[i+1]
                args.remove(args[i])
                args.remove(args[i])
                mm = tuple(map(int, mm.split("-")))
                if self.valid_date(mm, "m", True):
                    self.MM = range(*mm)
            except Exception as Error:
                print(Error)

        if "-dd" in args:
            try:
                i = args.index("-dd")
                dd = args[i+1]
                args.remove(args[i])
                args.remove(args[i])
                dd = tuple(map(int, dd.split("-")))
                if self.valid_date(dd, "d"):
                    self.DD = range(*dd)
            except Exception as Error:
                print(Error)

        if "-fd" in args:
            try:
                i = args.index("-fd")
                fd = args[i+1]
                args.remove(args[i])
                args.remove(args[i])
                self.FOUND_DIR = fd
            except Exception as Error:
                print(Error)

        return args

    def valid_date(self,
                   data: Union[List[int], Tuple[int, int]],
                   dtype: str,
                   out: bool = True) -> bool:

        dtype = dtype.lower().strip()
        if "m" in dtype:
            valid = range(1, 13)
        elif "d" in dtype:
            valid = range(1, 32)

        try:
            return ((int(data[0]) in valid) and (int(data[-1]) in valid))
        except Exception as Error:
            print(Error)

    def __init__(self, args: Union[List[str], Tuple[str]]) -> None:

        args = self._argParse(args)

        if len(args) <= 1:
            print(f"Usage: python {argv[0]} query -ARGV")
            self.query = self.Get_Query()
        else:
            self.query = S.join(args[1:])

        self.query = self.__template_query(self.query)
        self.query = tuple(map(
            self.transcript,
            self.query
        ))

        if not exists(self.FOUND_DIR):
            mkdir(self.FOUND_DIR)

        fileN = f"{self.FOUND_DIR}/{self.query[0]}_{len(self.query)}.txt"
        if exists(fileN):
            try:
                remove(fileN)
            except Exception as Error:
                print(Error)

        self.file_handle = open(fileN, "a")

        self.Start_Search()

    def __del__(self) -> None:

        try:
            with open(self.file_handle.name) as f:
                urls = f.read().split(PROTOCOL)
            with open(self.file_handle.name, "w") as f:
                f.write("\n"+PROTOCOL.join(sorted(urls)))
            self.file_handle.close()
            Run_Time = round(perf_counter() - self.startIn, 1)

            inf = (f"{self.TOTAL} - Found",
                   f"Run time: {Run_Time} seconds")
            print(*inf, sep=" | ")

        except AttributeError:
            print("\nExit...")
        except Exception as Error:
            print(Error)
        else:
            if TGPhind.openResult:
                from os import getcwd, startfile
                from os.path import join
                file_name = join(getcwd(), self.file_handle.name)
                startfile(file_name)


S = " "


PROTOCOL = "https://"
SITES = [
    "telegra.ph/", "te.legra.ph/", "graph.org/"]


def try_sites():
    threads = tuple()
    for url in SITES[1:]:
        thread = Thread(target=TGPhind.try_mirrors, args=(url,))
        thread.start()

        threads += thread,
    for thread in threads:
        thread.join()


if "-noMirrors" in argv:
    SITES = SITES[0],
    argv.remove("-noMirrors")
else:
    try_sites()

SITES = tuple(SITES)

if __name__ == "__main__":

    TGPhind.argv_Parse()
    TGPhind.print_preview()

    if "-noOut" in argv:
        print_ = print
        def print(*args, **kwargs): pass
        argv.remove("-noOut")
    if "--" in argv:
        punctuation = punctuation.replace("-", "")
        argv.remove("--")

    TGPhind(argv)
