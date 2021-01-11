from threading import Thread
from os import system, name
from sys import argv, stdout

try:
    import requests
except ModuleNotFoundError:
    system('pip install requests')
    import requests

stdout.write('\033[0m')
system("git pull")
system("cls" if name == "nt" else "clear")


def transcript(rurl):
    rurl = rurl.lower()
    rurl = rurl.replace(' ', '-')

# Буквы русского алфавита:
    rurl = rurl.replace('а', 'a')
    rurl = rurl.replace('б', 'b')
    rurl = rurl.replace('в', 'v')
    rurl = rurl.replace('г', 'g')
    rurl = rurl.replace('д', 'd')
    rurl = rurl.replace('е', 'e')
    rurl = rurl.replace('ё', 'yo')
    rurl = rurl.replace('ж', 'zh')
    rurl = rurl.replace('з', 'z')
    rurl = rurl.replace('и', 'i')
    rurl = rurl.replace('й', 'j')
    rurl = rurl.replace('к', 'k')
    rurl = rurl.replace('л', 'l')
    rurl = rurl.replace('м', 'm')
    rurl = rurl.replace('н', 'n')
    rurl = rurl.replace('о', 'o')
    rurl = rurl.replace('п', 'p')
    rurl = rurl.replace('р', 'r')
    rurl = rurl.replace('с', 's')
    rurl = rurl.replace('т', 't')
    rurl = rurl.replace('у', 'u')
    rurl = rurl.replace('ф', 'f')
    rurl = rurl.replace('х', 'h')
    rurl = rurl.replace('ц', 'c')
    rurl = rurl.replace('ч', 'ch')
    rurl = rurl.replace('ш', 'sh')
    rurl = rurl.replace('щ', 'shch')
    rurl = rurl.replace('ъ', '')
    rurl = rurl.replace('ы', 'y')
    rurl = rurl.replace('ь', '')
    rurl = rurl.replace('э', 'eh')
    rurl = rurl.replace('ю', 'yu')
    rurl = rurl.replace('я', 'ya')

# Символы:
    rurl = rurl.replace('!', '')
    rurl = rurl.replace('?', '')
    rurl = rurl.replace(',', '')
    rurl = rurl.replace('.', '')
    rurl = rurl.replace('*', '')
    rurl = rurl.replace('_', '')

    return rurl


if len(argv) <= 1:
    stdout.write('Использование:\n $ python ' + str(argv[0]) + ' [Запрос]\n')
    preus = input('Введите запрос сюда: ')
else:
    preus = ' '.join(argv[1:])

global use0, use1, lnkss, mlnk, lnk0, lnk1, srch

srch = transcript(preus)
stdout.write(f'Запрос: {srch}\n')


stdout.write('Проверка зеркал...\n\n')

lnkss = ['http://te.legra.ph/', 'http://graph.org/', 'http://telegra.ph/']
lnk0 = lnkss[0]
lnk1 = lnkss[1]
mlnk = lnkss[2]

use0 = False
use1 = False

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

try:
    m = requests.get(mlnk, headers=headers)
    stdout.write(mlnk + ' ' + str(m) + '\n')
except Exception as no:
    stdout.write(str(no) + '\n')
    exit()
else:
    if not (m.status_code >= 100 and m.status_code <= 400):
        exit()

try:
    m = requests.get(lnk0, headers=headers)
    stdout.write(lnk0 + ' ' + str(m) + '\n')
except Exception as no:
    stdout.write(str(no) + '\n')
    use0 = False
else:
    if m.status_code >= 100 and m.status_code <= 400:
        use0 = True
try:
    m = requests.get(lnk1, headers=headers)
    stdout.write(lnk1 + ' ' + str(m) + '\n')
except Exception as no:
    stdout.write(str(no) + '\n')
    use1 = False
else:
    if m.status_code >= 100 and m.status_code <= 400:
        use1 = True

stdout.write('Проверка завершена, мой вердикт:\n\n')

if use0:
    stdout.write(lnkss[0] + ' - Работает нормально.\n')
else:
    stdout.write(lnkss[0] + ' - Не работает.\n')

if use1:
    stdout.write(lnkss[1] + ' - Работает нормально.\n')
else:
    stdout.write(lnkss[1] + ' - Не работает.\n')

del(lnkss)


def mor(glnk):
    n = 2
    fi = open(f'{srch}.txt', 'a')
    while 1:
        lnk = f'{glnk}-{n}'
        g = requests.get(lnk)
        stdout.write('\033[34m' + lnk + ' ' + str(g) + '\n')
        n += 1
        if g.status_code >= 300:
            break
        else:
            fi.write(f'\n{lnk}\n')
            if use0:
                lnkm = glnk.replace(mlnk, lnk0) + '\n'
                fi.write(f'\n{lnkm}')
            if use1:
                lnkm = glnk.replace(mlnk, lnk1) + '\n\n'
                fi.write(f'\n{lnkm}')


def main_search(mm, dd):
    try:
        try:
            mm = str(mm).rjust(2, '0')
            dd = str(dd).rjust(2, '0')
            lnk = f'{mlnk}{srch}-{mm}-{dd}'
            g = requests.get(lnk)
            if g.status_code <= 300:
                col = '\033[32m'
                glnk = lnk
                stdout.write(col + lnk + ' ' + str(g) + '\n')
                mor(glnk)
                while 1:
                    try:
                        with open(f'{srch}.txt', 'a') as f:
                            f.write(f'{lnk}\n')
                        break
                    except:
                        pass
                if use0:
                    lnkm = glnk.replace(mlnk, lnk0) + '\n'
                    while 1:
                        try:
                            with open(f'{srch}.txt', 'a') as f:
                                f.write(lnkm)
                            break
                        except:
                            pass
                if use1:
                    lnkm = glnk.replace(mlnk, lnk1) + '\n\n'
                    while 1:
                        try:
                            with open(f'{srch}.txt', 'a') as f:
                                f.write(lnkm)
                            break
                        except:
                            pass
            else:
                col = '\033[31m'
                stdout.write(col + lnk + ' ' + str(g) + '\n')

        except Exception as Err:
            stdout.write(str(Err) + '\n')
    except Exception as er:
        stdout.write(str(er) + '\n')


if __name__ == '__main__':
    stdout.write(
        '\033[34mДождитесь окончантя поиска!\nИ введите коммманду python file-sort.py\n')
    for mm in range(1, 13):
        for dd in range(1, 32):
            while 1:
                try:
                    thrd = Thread(target=main_search, args=(mm, dd))
                    thrd.start()
                    break
                except:
                    pass

with open('result', 'w') as f:
    f.write(f'{srch}.txt')
