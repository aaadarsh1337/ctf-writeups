codes = open('mazehex').read().strip().replace(' ', '')
codes = bytes.fromhex(codes)

j = 0

while j < len(codes)//4:
	for i in range(0, len(codes), 4):
		if j % 16 == 0 and j != 0:
			print()
		j += 1
		if codes[i:i+4] == b'\x81\xfb\x000':
			print("#", end='')
		elif codes[i:i+4] == b'0\x00\x00\x00':
			print(" ", end='')
		elif codes[i:i+4] == b'\x81\x7f\x050':
			print("+", end='')
		elif codes[i:i+4] == b'\x81t\x050':
			print("-", end='')
		elif codes[i:i+4] == b'\x81\x85\x050':
			print("E", end='')
		else:
			print(codes[i:i+4])

