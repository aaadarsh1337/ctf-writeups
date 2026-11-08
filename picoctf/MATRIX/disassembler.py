import sys

codes = open('hexdump').read().replace(' ', '')
assembly = open('assembly', 'w')
codes = bytes.fromhex(codes)

i = 0

stack = bytearray()
result = bytearray(4)
stack2 = bytearray()

def vmpush(value, s=False):
	global stack
	stack.extend(value.to_bytes(2, 'little', signed=s))

while i < len(codes):

	pc = i
	op = codes[i]

	if op == 0:
		assembly.write('NOP\n')
		i += 1

	if op == 0x80:
		value = int.from_bytes(codes[i + 1:i + 2], "little", signed=True)
		vmpush(value, True)
		assembly.write(f"PUSH {hex(value)}\n")
		i += 2

	elif op == 0x81:
		value = int.from_bytes(codes[i+1:i+3], 'little')
		vmpush(value)
		assembly.write(f"PUSH {hex(value)}\n")
		i += 3

	elif op == 0x30:
		i = int.from_bytes(stack[-2:], 'little')
		del stack[-2:]
		assembly.write(f"POP <{hex(i)}>\n")
		assembly.write(f"JMP {hex(i)}\n")

	elif op == 0x10:
		value = int.from_bytes(stack[-2:], 'little')
		vmpush(value)
		assembly.write(f"PUSH {hex(value)}\n")
		i += 1


	elif op == 0x31:
		value = int.from_bytes(stack[-2:], 'little')
		condtn = int.from_bytes(stack[-4:-2], 'little')

		del stack[-4:]
		assembly.write(f"POP <{hex(value)}>\n")
		if condtn == 0:
			assembly.write(f"JMP {hex(value)}\n")
			i = value
		else:
			i += 1
		
	elif op == 0xc1:
		val = int.from_bytes(stack[-2:], 'little')
		print(chr(val & 0xFF), end='')
		assembly.write(f"PUTC <{chr(val & 0xFF)}>\n")
		i += 1
		assembly.write(f"POP <{hex(val)}>\n")
		del stack[-2:]


	elif op == 0xc0:
		assembly.write("GETC\n")
		guess = sys.stdin.read(1)
		value = ord(guess[0])
		vmpush(value)
		i += 1
		assembly.write(f"PUSH {guess}\n")

	elif op == 0x13:
		value = int.from_bytes(stack[-4:-2], 'little')
		value2 = int.from_bytes(stack[-2:], 'little')
		valuef = (value - value2) & 0xFFFF

		t = int.from_bytes(stack[-4:], 'little')
		
		del stack[-4:]

		vmpush(valuef)
		assembly.write(f"SUB {hex(value)} {hex(value2)}\n")
		assembly.write(f"POP <{hex(t)}>\n")
		assembly.write(f"PUSH {hex(valuef)}\n")
		i += 1

	elif op == 0x1:
		value = int.from_bytes(stack[-2:], "little")
		assembly.write(f"POP <{(value)}>\n")
		del stack[-2:]

		result[0] = 0
		result[2:4] = value.to_bytes(2, 'little')
		assembly.write(f"MODIFY result --> {result}\n")
		break

	elif op == 0x11:
		assembly.write(f"POP <{(stack[-2:])}>\n")
		del stack[-2:]
		i += 1

	elif op == 0x20:
		value = int.from_bytes(stack[-2:], 'little')
		stack2.extend(value.to_bytes(2, 'little'))
		assembly.write(f"POP <{hex(value)}> <from stack1>\n")
		assembly.write(f"PUSH {hex(value)} <to stack2>\n")
		del stack[-2:]

		i += 1

	elif op == 0x21:
		value = int.from_bytes(stack2[-2:], 'little')
		vmpush(value)
		assembly.write(f"POP <{hex(value)}> <from stack2>\n")
		assembly.write(f"PUSH {hex(value)} <to stack1>\n")
		del stack2[-2:]

		i += 1


	elif op == 0x12:
		value = int.from_bytes(stack[-4:-2], 'little')
		value2 = int.from_bytes(stack[-2:], 'little')
		valuef = value + value2
		valuef &= 0xFFFF
		assembly.write(f'ADD {hex(value)} {hex(value2)}\n')
		assembly.write(f"POP <{hex(int.from_bytes(stack[-4:], 'little'))}>\n")
		assembly.write(f"PUSH {hex(valuef)}\n")
		del stack[-4:]

		vmpush(valuef)

		i += 1

	elif op == 0x14:
		edx = int.from_bytes(stack[-4:-2], 'little')
		ecx = int.from_bytes(stack[-2:], 'little')
		assembly.write(f"XCHANGE {hex(edx)} {hex(ecx)}\n")
		stack[-4:-2] = ecx.to_bytes(2, 'little')
		stack[-2:] = edx.to_bytes(2, 'little')
		i += 1
