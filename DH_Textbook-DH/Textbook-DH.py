#!/usr/bin/python3
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import hashlib
import random


class Person(object):
    def __init__(self, p):
        self.p = p
        self.g = 2

    def set_shared_key(self, k):
        self.sk = pow(k, 2, self.p)
        aes_key = hashlib.md5(str(self.sk).encode()).digest()
        self.cipher = AES.new(aes_key, AES.MODE_ECB)

    def encrypt(self, pt):
        return self.cipher.encrypt(pad(pt, 16)).hex()

    def decrypt(self, ct):
        return unpad(self.cipher.decrypt(bytes.fromhex(ct)), 16)


prime = int("0xba3a42e162ea5cc3ec3f0442885aee6daea1587b7e41aafe17f5b430d81446cdc056b6064e5fc51b3a7741b45bea04c9ab78856cf3ec43f9f696b537f81b61416a49942fb3f452e556a02957f981e047ad81123841baabeb259cb05c40052aca888bc0169bb5c61bd7544520053f4f7570faaa1546cb282bf50d94da0f752455", 16)
Alice = Person(prime)
Bob = Person(prime)

Alice.set_shared_key(int("0x4e194c4499bcd77d8ec50f83e655affe71978e102935e660e8ff82e09d026d10b70636208bcc69f19ac6bc75adefad39646dc378178341c0d5e8d03b5b3901d02e0acdcc4642cedfa3e8edf42b54bd542e7e5fd827f42a66e9b6a0063db2d941fd583f081c3a622e4e5ee7092ea88391762cb8e7ab7082bf8c86874528bfc1ae", 16))
Bob.set_shared_key(int("0xb3604328842554c9dc1b4e6c95c7d34e5429f8696746255d8a989b01f630ecf36cc075569a43fdd175c231d3180755726989b0bbe974ff801ea15aaa2cae5ae80e74c4d6647014b47a4687f3cfdc318a86e4c006746f10640ab2297b00811f7a7b2306743fc75428a3ca2d4fc3ff95b5b209932291823781ec518e4abbb4edd3", 16))

print(Alice.decrypt(
    "800f988b6633c40ae37f9cc2c71f4e4f26d1165a8c870c902f39e679f62c7e3717fd023d0c66a7f46b037ccb97c93d47"))
print(Bob.decrypt(
    "d7eef4eab8e7c28a70e23797044df9bf92fece19f6129975630833c229f84e86a61bafaf14db4b501c39a64186119771"))
