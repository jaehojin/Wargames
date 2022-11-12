from Crypto.Util.number import *

message = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
msg_hex = hex(message)
msg_list = []
for i in range(1, int(len(msg_hex)/2)):
    msg_list.append(chr(int(msg_hex[i*2:(i+1)*2], 16)))
print(message)
print("".join(msg_list))
print(msg_hex)
#base16_msg = long_to_bytes(message)
