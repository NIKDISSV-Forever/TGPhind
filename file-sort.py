ll = []

with open('result', 'r') as f:
	fn = f.read()

with open(fn, 'r') as f:
	for l in f:
		ll.append(l)
with open(fn, 'w') as f:
	f.write('')

with open(fn, 'a') as f:
	for lin in sorted(ll):
		if lin[:7] == 'http://':
			f.write(lin)
		else:
			pass
