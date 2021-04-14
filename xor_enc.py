

class XorMsg:

    def __init__(self, keys: tuple):

        self._enc_keys = []
        for key in keys:
            self._enc_keys.insert(-1, key)

        self.keys_left = bool(len(self._enc_keys))

    def encrypt(self, msg) -> bytes:

        ba = bytearray()
        for b in msg:
            b_xor = chr(ord(b)) ^ chr(ord())


