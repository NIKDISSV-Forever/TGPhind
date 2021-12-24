from typing import Iterator

BRACKET1, BRACKET2 = '<>'

__all__ = 'set_brackets', 'parse', 'join'


def set_brackets(l: str, r: str = None):
    if not r:
        l, r = l[:2]
    global BRACKET1
    if l != BRACKET1:
        BRACKET1 = l
    global BRACKET2
    if r != BRACKET2:
        BRACKET2 = r


def parse(line: str) -> Iterator[str]:
    a = line.find(BRACKET1) + 1
    if not (a and line):
        yield line
        return
    tmp = for_rep = line[a:line.find(BRACKET2)]
    if not tmp:
        yield line
        return
    len_tmp = len(tmp)
    if len_tmp == 1:
        letters = '', tmp
    elif len_tmp == 3:
        tmp1 = tmp[1]
        letters = tuple(chr(i)
                        for i in range(ord(tmp[0]), ord(tmp[2]) + 1, int(tmp1)
        if tmp1.isdigit() else 1)
                        )
    else:
        letters = tmp
    for letter in letters:
        yield from parse(line.replace(f'{BRACKET1}{for_rep}{BRACKET2}',
                                      letter))


def join(protocol: str, host: str, path: str) -> str:
    return f'{protocol}://{host}/{path}'
