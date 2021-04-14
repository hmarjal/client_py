

def get_parity(n):
    while n > 1:
        n = (n >> 1) ^ (n & 1)
    return n


def add_parity(mjono):

    ret = ""
    for c in mjono:
        c = ord(c)
        c <<= 1
        c += get_parity(c)
        ret = ret + chr(c)
    return ret


"""
sana = "abcde"
for _ in sana:
    print(bin(ord(_)))


sana_parity = add_parity(sana)

print(sana_parity)

for _ in sana_parity:
    print(bin(ord(_)))
"""
