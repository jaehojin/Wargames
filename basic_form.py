from pwn import *

# context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./chall")
else:
    PORT = int(input("PORT: "))
    HOST = int(input("HOST: "))
    p = remote("host" + str(HOST) + ".dreamhack.games", PORT)


def slog(name, addr):
    return success(name + ": " + str(hex(addr)))


# To send bytes: p.sendline(p64(payload))
# To send numbers: p.sendline(str(payload)) <- i.e.) payload = 0xFFFFFFFF
