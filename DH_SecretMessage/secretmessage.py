from pwn import *
def slog(name, addr):
	return success(": ".join([name, hex(addr)]))

context.log_level = "debug"

LOCAL = True
if LOCAL:
	p = process("./prob")
else:
	PORT = int(input("Port: "))
	HOST = int(input("Host: "))
	p = remote("host" + str(HOST) + ".dreamhack.games", PORT)

elf = ELF("./prob")

width = 500
height = 50
size = width * height

f = open("./secretMessage.raw", "wb")

secretMessage = b""
for i in range(int(size/5)):
	secretMessage += b"\xFF"
	secretMessage += b"\xFF"
	secretMessage += b"\xFE"
	secretMessage += b"\xFF"
	secretMessage += b"\xFE"

secretMessageArr = bytearray(secretMessage)
f.write(secretMessageArr)
f.close()
