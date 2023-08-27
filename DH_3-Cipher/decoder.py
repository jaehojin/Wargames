from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 1. RSA
ac_key_rsa_hex = "0x6222FEF4DCC247E7"
ac_key_rsa = int(ac_key_rsa_hex, 16)


def extendedEuclidean(n, b):
    r1, r2 = n, b
    t1, t2 = 0, 1
    while r2:
        q = r1 // r2
        r = r1 - q * r2
        r1, r2 = r2, r
        t = t1 - q * t2
        t1, t2 = t2, t

    if r1 != 1:
        return 0
    if t1 < 0:
        t1 = n + t1
    return t1


p = 3573716833
q = 3671005097
e = 65537
n = 13119132709177697801
#   1803412828046968577
phi = (p - 1) * (q - 1)
d = extendedEuclidean(phi, e)
print(d)

aes_key = pow(ac_key_rsa, d, n)

# 2. AES CBC
iv_encoded = "0xOvbqbbU5fciYTMpaN8yw=="
ciphertext_encoded = "OQfnFGzd2lWUsV+OdVHWzep/WZxKWLbmmG2wx1iuBaP0eXREE/JXcbE7rkgmHl9aj3Q2TwyIVIswk8V106S6HIJoS2/5LziJT+WN5AqS7Hs="
aes_iv = b64decode(iv_encoded)
aes_ciphertext = b64decode(ciphertext_encoded)
print(aes_iv)
print(aes_ciphertext)

print(len(aes_iv))
print(len(bytes(aes_key)))

aes_cipher = AES.new(bytes(aes_key), AES.MODE_CBC, aes_iv)
plaintext = unpad(aes_cipher.decrypt(aes_ciphertext), AES.block_size)
print(plaintext)
