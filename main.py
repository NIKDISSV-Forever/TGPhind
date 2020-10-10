print('\033[0m')
from transcript import transcript
from sys import argv
from os import system
system('git pull; clear')
from threading import Thread
try:
	import requests
except ModuleNotFoundError:
	system('pip install requests')
	import requests

if len(argv) <= 1:
	print('Использование:\n $ python', + argv[0], '[Запрос]')
	preus = input('Введите запрос сюда: ')
else:
	preus = ' '.join(argv[1:])

global use0, use1, lnkss, mlnk, lnk0, lnk1, srch

srch = transcript(preus)
print(f'Запрос: {srch}')


print('Проверка зеркал...\n')

lnkss = ['http://te.legra.ph/', 'http://graph.org/', 'http://telegra.ph/']
lnk0 = lnkss[0]
lnk1 = lnkss[1]
mlnk = lnkss[2]

use0 = False
use1 = False

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

try:
	m = requests.get(mlnk, headers=headers)
	print(mlnk, m)
except Exception as no:
	print(no)
	exit()
else:
	if m.status_code >= 100 and m.status_code <= 400:
		pass
	else:
		exit()

try:
	m = requests.get(lnk0, headers=headers)
	print(lnk0, m)
except Exception as no:
	print(no)
	use0 = False
else:
	if m.status_code >= 100 and m.status_code <= 400:
		use0 = True
try:
	m = requests.get(lnk1, headers=headers)
	print(lnk1, m)
except Exception as no:
	print(no)
	use1 = False
else:
	if m.status_code >= 100 and m.status_code <= 400:
		use1 = True

print('Проверка завершена, мой вердикт:')
print()
if use0:
	print(lnkss[0], '- Работает нормально.')
else:
	print(lnkss[0], '- Не работает.')

if use1:
	print(lnkss[1], '- Работает нормально.')
else:
	print(lnkss[1], '- Не работает.')

del(lnkss)

def mor(glnk):
	n = 2
	fi = open(f'{srch}.txt', 'a')
	while 1:
		lnk = f'{glnk}-{n}'
		g = requests.get(lnk)
		print('\033[34m', lnk, g)
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
				print(col, lnk, g)
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
				print(col, lnk, g)
						
		except Exception as Err:
			print(Err)
	except Exception as er:
		print(er)
if __name__ == '__main__':
	print('\033[34mДождитесь окончантя поиска!\nИ введите коммманду python file-sort.py')
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
