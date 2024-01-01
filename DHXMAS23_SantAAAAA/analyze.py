import re

nato = [
    "Alpha",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliett",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Whiskey",
    "X-ray",
    "Yankee",
    "Zulu",
]

nato = [alpha.upper() for alpha in nato]
nato_convert = []
for alpha in nato:
    print(alpha)
    alpha_conv = ""
    for letter in alpha:
        if ord("A") > ord(letter) or ord(letter) > ord("Z"):
            continue
        alpha_conv += f"{re.sub('[A-Z]', 'A', nato[ord(letter) - ord('A')])} "
    alpha_conv = alpha_conv[:-1]
    # alpha_conv += f"{re.sub('[A-Z]', 'A', alpha)}"
    nato_convert.append(alpha_conv)

print(nato_convert)

with open("A.txt", "r") as f:
    data = f.readline()
data = data.split("  ")

"""
result = ""
for alpha in data:
    try:
        result += chr(ord("A") + nato_convert.index(alpha))
    except Exception:
        print(f"[*] {alpha}")
"""

print(result)
