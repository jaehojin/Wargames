from pwn import *

context.log_level = "debug"

LOCAL = True
if LOCAL:
    p = process("./robot_only.py")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)

p.sendlineafter("> ", b"2")
p.recvuntil(": \"")
verify = p.recv()
p.sendlineafter("> ", verify[:len(verify)-1])

p.interactive()
