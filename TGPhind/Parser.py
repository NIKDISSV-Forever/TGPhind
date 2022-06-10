from typing import Iterator

__all__ = 'parse', 'join'


def parse(line: str, brackets='<>') -> Iterator[str]:
    bl, br, *_ = brackets
    a = line.find(bl) + 1
    if not (a and line):
        yield line
        return
    tmp = for_rep = line[a:line.find(br)]
    if not tmp:
        yield line
        return
    len_tmp = len(tmp)
    if len_tmp == 1:
        letters = '', tmp
    elif len_tmp == 3:
        tmp1 = tmp[1]
        letters = tuple(chr(i)
                        for i in range(ord(tmp[0]), ord(tmp[2]) + 1, int(tmp1) if tmp1.isdigit() else 1))
    else:
        letters = tmp
    for letter in letters:
        yield from parse(line.replace(f'{bl}{for_rep}{br}', letter))


def join(protocol: str, host: str, path: str) -> str:
    return f'{protocol}://{host}/{path}'
