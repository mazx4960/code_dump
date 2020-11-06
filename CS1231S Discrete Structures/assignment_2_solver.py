n = 6
x = y = [i for i in range(n)]
a = [i + 1 for i in range(n - 1)]

for i in x:
	print('X Value:', i)
	for j in y:
		for k in a:
			if (k * i) % n == (k * j) % n:
				print('Match: y ', j, 'a', k)
				break
	print()
