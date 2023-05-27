hex_list = [(hex(i)[2:].zfill(2).upper()) for i in range(256)]
print(hex_list)

plain_s = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEF"

plain_list = [hex(ord(i))[2:].zfill(2).upper() for i in plain_s]
print(plain_list)

enc_list = list(range(len(plain_list)))
print(enc_list)

for i in range(len(plain_list)):
    hex_b = plain_list[i]
    index = hex_list.index(hex_b)
    enc_list[i] = hex_list[(index + 128) % len(hex_list)]
print(enc_list)
