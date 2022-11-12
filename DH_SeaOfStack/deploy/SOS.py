from pwn import *

#context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./prob")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)

elf = ELF("./prob")
libc = ELF("./libc.so.6")
