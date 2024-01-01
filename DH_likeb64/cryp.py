import binascii


def string_to_bits(s):
    return "".join(format(ord(c), "08b") for c in s)


text = "IREHWYJZMEcGCODGMMbTENDDGcbGEMJZGEbGEZTFGYaGKNRTMIcGIMBSGRQTSNDDGAaWGYZRHEbGCNRQMUaDOMbEMRTGEYJYGUaWGOJQMYZHa==="

buffer = []
for i in range(len(text) // 8):
    buffer.append(text[i * 8 : (i + 1) * 8])
print(buffer)

standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
indices = []
for i in buffer:
    bit_text = ""
    for letter in i:
        if letter == "=":
            
        else: