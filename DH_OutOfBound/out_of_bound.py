from pwn import *
def slog(name, addr):
	return success(": ".join([name, hex(addr)]))

# Local
p = process("./out_of_bound")

# Online
PORT = int(input("Port: "))
HOST = int(input("Host: "))
p = remote("host" + str(HOST) + ".dreamhack.games", PORT)

elf = ELF("./out_of_bound")

p.recvuntil("")
