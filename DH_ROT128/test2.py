hex_list = [(hex(i)[2:].zfill(2).upper()) for i in range(256)]

enc_s = [0x09, 0xD0, 0xCE, 0xC7, 0x8D]

enc_list = [hex(i)[2:].zfill(2).upper() for i in enc_s]

dec_list = list(range(len(enc_list)))

for i in range(len(enc_list)):
    hex_b = enc_list[i]
    index = hex_list.index(hex_b)
    dec_list[i] = hex_list[(index - 128) % len(hex_list)]

dec_list = "".join(dec_list)

print(dec_list)
