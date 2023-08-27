#!/usr/bin/env python3
import os
from cipher import NTRU

def menu():
    print("\n!Guessing Game!\n")
    print("1. Play Game")
    print("2. Exit")
    return

def bye(msg):
    print(msg)
    exit()

def give_flag():
    with open("flag", "rb") as f:
        flag = f.read()
    print(flag)

def game(cipher: NTRU):
    m1 = bytes.fromhex(input("Your message(hex)> "))
    assert len(m1) == 10
    m2 = os.urandom(10)
    choice = int.from_bytes(os.urandom(1), 'big') % 2
    picked = [m1, m2][choice]

    c = cipher.encrypt(picked)
    print(f'Encrypted = \n{c.hex()}\n')
    print('Which one is encrypted? ')
    print(f'1. {m1.hex()}')
    print(f'2. {m2.hex()}')

    i = int(input("> "))
    chk = i-1 == choice

    return chk

def main():
    win_n = 0
    game_n = 0
    cipher = NTRU(N=509, p=3, q=2048, verbose=True)
    while True:
        menu()
        i = int(input("> "))
        if i == 1:
            chk = game(cipher)
            game_n += 1
            if chk:
                print("Correct!")
                win_n += 1
            else:
                print("Wrong...")
        elif i == 2 :
            if game_n >= 20 and win_n/game_n > 0.99:
                give_flag()
            bye("Ok, Bye~")
        else:
            bye("Invalid option.")

if __name__ == '__main__':
    main()
