import secrets


class XorCrypt:

    def __init__(self, decryption_keys: list):
        self.__encryption_keys = self.__generate_keys()
        self.__decryption_keys = decryption_keys[:]

    @staticmethod
    def __generate_keys() -> list:
        encrpytion_keys = []
        for n in range(20):
            encryption_word = secrets.token_bytes(64)
            encrpytion_keys.append(encryption_word)
        return encrpytion_keys

    def enc_keys_left(self) -> bool:
        return bool(self.__encryption_keys)

    def dec_keys_left(self) -> bool:
        return bool(self.__decryption_keys)

    def encrypt(self, data: bytes) -> bytes:
        if self.enc_keys_left():
            ba = bytearray()
            enc_key = self.__encryption_keys.pop(0)
            for i, b in enumerate(data):
                b_xor = b ^ enc_key[i]
                ba.append(b_xor)
            return bytes(ba)
        else:
            return data

    def decrypt(self, data: bytes) -> bytes:
        if self.dec_keys_left():
            ba = bytearray()
            dec_key = self.__decryption_keys.pop(0)
            for i, b in enumerate(data):
                b_xor = b ^ dec_key[i]
                ba.append(b_xor)
            return bytes(ba)
        else:
            return data

