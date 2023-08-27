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
