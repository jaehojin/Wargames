import time
from pwn import *


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))

#context.log_level = "debug"


f = open("\x0a", "wb")
f.write(b"\x00\x00\x00\x00")
f.close()

argv_list = ["" for i in range(100)]
argv_list[1] = b"0>"+b"\x00\x0a\x00\xff"
argv_list[2] = b"2>"+b"\x00\x0a\x02\xff"
argv_list[ord('A')] = b"\x00"
argv_list[ord('B')] = b"\x20\x0a\x0d"


LOCAL = False
if LOCAL:
    p = process("./input")
else:
    s = ssh("input2", "pwnable.kr", 2222, "guest")
    p = s.process(executable="./input", argv=argv_list,
                  env={b'\xde\xad\xbe\xef': b'\xca\xfe\xba\xbe'})

log.info(p.recvline())
log.info(p.recvline())
log.info(p.recvline())

print(argv_list)

for i in range(5):
    sleep(5)
    msg = p.recvline()
    log.info(msg)
