

def get_parity(n) -> int:
    while n > 1:
        n = (n >> 1) ^ (n & 1)
    return n


def check_parity(msg) -> bool:
    if isinstance(msg, bytes):
        msg = msg.decode('utf-8')
    for c in msg:
        c = ord(c)
        parity_bit = (c & 1)
        c >>= 1
        parity_check = get_parity(c)
        if parity_check != parity_bit:
            return False
    return True


def add_parity(msg) -> str:
    if isinstance(msg, bytes):
        msg = msg.decode('utf-8')
    ret = ""
    for c in msg:
        c = ord(c)
        c <<= 1
        c += get_parity(c)
        ret = ret + chr(c)
    return ret


def remove_parity(msg) -> str:
    if isinstance(msg, bytes):
        msg = msg.decode('utf-8')
    ret = ""
    for c in msg:
        c = ord(c)
        c >>= 1
        ret = ret + chr(c)
    return ret
