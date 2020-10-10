with open('result', 'r') as f:
	fn = f.read()

with open(fn, 'a') as f:
	for lin in sorted(ll):
		if lin[:7] == 'http://':
			f.write(lin)
		else:
			pass
