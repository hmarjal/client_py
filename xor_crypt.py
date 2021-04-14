

class XorMsg:

    def __init__(self, enc_keys: list, dec_keys: list):
        self._enc_keys = enc_keys[:]
        self._dec_keys = dec_keys[:]

    def enc_keys_left(self) -> bool:
        return bool(self._enc_keys)

    def dec_keys_left(self) -> bool:
        return bool(self._dec_keys)

    def encrypt(self, msg: bytes) -> bytes:
        if self.enc_keys_left():
            ba = bytearray()
            enc_key = self._enc_keys.pop(0)
            for i, b in enumerate(msg):
                b_xor = ord(b) ^ ord(enc_key[i])
                ba.insert(0, b_xor)
            return bytes(ba)
        else:
            return msg

    def decrypt(self, msg: bytes) -> bytes:
        if self.dec_keys_left():
            ba = bytearray()
            dec_key = self._dec_keys.pop(0)
            for i, b in enumerate(msg):
                b_xor = ord(b) ^ ord(dec_key[i])
                ba.insert(0, b_xor)
            return bytes(ba)
        else:
            return msg

