#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__banner__ = """

  _____ ____ ____  _     _           _ 
 |_   _/ ___|  _ \| |__ (_)_ __   __| |
   | || |  _| |_) | '_ \| | '_ \ / _` |
   | || |_| |  __/| | | | | | | | (_| |
   |_| \____|_|   |_| |_|_|_| |_|\__,_|
                                       

"""
__author__ = "NIKDISSV"


from urllib.request import urlopen
from threading import Thread

from os import mkdir, remove
from os.path import exists
from sys import argv

from typing import Union, List, Tuple, Dict
from string import punctuation


S = " "
TRANSCRIPT_DICT = dict(zip(
    ("а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я "
     + S.join(punctuation)).split(S),
    ("a b v g d e yo zh z i j k l m n o p r s t y f h c ch sh shch  y  eh yu ya "
     + S*len(punctuation)).split(S)))
TRANSCRIPT_DICT[S] = "-"


SITES = ["https://telegra.ph/", "https://te.legra.ph/", "https://graph.org/"]
for url in SITES[1:]:
    try:
        resp = urlopen(url)
    except Exception as Error:
        SITES.remove(url)
        print(url, Error)
    else:
        print(url, resp.getcode())
SITES = tuple(SITES)


class TGPhind:

    MM = range(1, 13)
    DD = range(1, 32)

    FOUND_DIR = "found"

    TOTAL = 0

    def __init__(self, args: Union[List[str], Tuple[str]]) -> None:

        args = self._argParse(args)

        if len(args) <= 1:
            print(f"Usage: python {argv[0]} query -PARAMS")
            self.query = self.Get_Query()
        else:
            self.query = S.join(args[1:])
        self.query = self.transcript(self.query)

        if not exists(self.FOUND_DIR):
            mkdir(self.FOUND_DIR)

        fileN = f"{self.FOUND_DIR}/{self.query}.txt"
        if exists(fileN):
            try:
                remove(fileN)
            except Exception as Error:
                print(Error)

        self.file_handle = open(fileN, "a")

        self.Start_Search()

    def transcript(self,
                   text: str = "",
                   table: Dict[str, str] = TRANSCRIPT_DICT,
                   lowered: bool = True) -> str:
        text = str(text).lower() if lowered else str(text)
        table = dict(table)
        for i in table:
            if i in text:
                text = text.replace(i, table[i])
        return text

    def Get_Query(self) -> str:

        while True:
            query = input("Enter your search term: ").strip().lower()
            if query:
                break
            else:
                print("The line is empty!")
        return query

    def Start_Search(self) -> None:

        info = f"Query: {self.query} | MM: {self.MM[-1]} DD: {self.DD[-1]} | Found in: {self.FOUND_DIR}"
        print(info)

        for mm in self.MM:
            for dd in self.DD:
                mm, dd = str(mm).rjust(2, "0"), str(dd).rjust(2, "0")
                t = Thread(target=self.Search, args=(mm, dd))
                t.start()

    def Search(self,
               mm: Union[str, int], dd: Union[str, int], n: str = "") -> None:

        suf = f"{self.query}-{mm}-{dd}{n}"
        url = f"{SITES[0]}{suf}"

        try:
            resp = urlopen(url, )
        except Exception as Error:
            resp = Error
        code = resp.getcode()
        if code < 400:
            self.file_handle.write(url+"\n")
            self.TOTAL += 1
            for u in SITES[1:]:
                self.file_handle.write(f"{u}{suf}\n")
            self.Search(mm, dd, n=int(n)-1 if n else "-2")
        print(url, code)

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
        else:
            return False

        try:
            return ((int(data[0]) in valid) and (int(data[-1]) in valid))
        except Exception as Error:
            if out:
                print(Error)

    def __del__(self) -> None:

        try:
            with open(self.file_handle.name) as f:
                urls = f.read().split("\n")
            with open(self.file_handle.name, "w") as f:
                f.write("\n".join(sorted(urls)))
            self.file_handle.close()
            print(f"{self.TOTAL} - Found")
        except Exception as Error:
            print(Error)


if __name__ == "__main__":

    from os import system, name
    system("cls" if name == "nt" else "clear")
    print(__banner__)

    TGPhind(argv)
