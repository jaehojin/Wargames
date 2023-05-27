hex_list = [(hex(i)[2:].zfill(2).upper()) for i in range(256)]

with open("./encfile", "rb") as f:
    enc_s = f.read()

enc_list = [
    hex(int(chr(enc_s[i * 2]) + chr(enc_s[i * 2 + 1]), 16))[2:].zfill(2).upper()
    for i in range(int(len(enc_s) / 2))
]

dec_list = list(range(len(enc_list)))

for i in range(len(enc_list)):
    hex_b = enc_list[i]
    index = hex_list.index(hex_b)
    dec_list[i] = bytes.fromhex(hex_list[(index - 128) % len(hex_list)])

dec_list = b"".join(dec_list)

with open("flag.png", "wb") as f:
    f.write(dec_list)
