import secrets


class XorCrypt:

    def __init__(self):
        self.debug_count = 0
        self.encryption_keys = []
        self.decryption_keys = []
        self.decryption_keys_test = []
        self.enc_i = 0
        self.dec_i = 0
        for n in range(20):
            encryption_word = secrets.token_hex(32)
            self.encryption_keys.append(encryption_word)

    def add_decryption_keys(self, dec_keys):
        if not self.decryption_keys:
            for key in dec_keys:
                self.decryption_keys.append(key.decode('utf-8'))
        self.decryption_keys_test = self.decryption_keys[:]

    def enc_keys_left(self) -> bool:
        return bool(self.encryption_keys)

    def dec_keys_left(self) -> bool:
        return bool(len(self.decryption_keys) > 0)

    def decrypt_test(self, data, start=0):
        dec_key = self.decryption_keys_test[start]
        i = 0
        ret = ""
        for b in data:
            if i > 63:
                start += 1
                if start > 18:
                    break
                dec_key = self.decryption_keys_test[start]
                i = 0
            if isinstance(b, str):
                b_xor = chr(ord(b) ^ ord(dec_key[i]))
            else:
                b_xor = b ^ dec_key[i]
            ret += b_xor
            i += 1
        print("DEC MSG START AT KEY {}: {}".format(start, ret))

    def enc_key_test(self, data):
        for k, key in enumerate(self.encryption_keys):
            ret = ""
            for i, b in enumerate(data):
                if isinstance(b, str):
                    b_xor = chr(ord(b) ^ ord(key[i]))
                else:
                    b_xor = b ^ key[i]
                ret += b_xor
            print("Key: {}\nENC MSG: {}".format(k, ret))

    def encrypt_mul(self, data):
        data_split = [data[s:s + 64] for s in range(0, len(data), 64)]
        ret = ""
        for chunk in data_split:
            if self.enc_keys_left():
                enc_key = self.encryption_keys.pop(0)
                i = 0
                for b in chunk:
                    b_xor = chr(ord(b) ^ ord(enc_key[i]))
                    ret += b_xor
                    i += 1
            else:
                ret += chunk
            return ret

    def decrypt_mul(self, data, total_len):
        data_split = [data[s:s+64] for s in range(0, len(data), 64)]
        ret = ""
        for chunk in data_split:
            if self.dec_keys_left():
                dec_key = self.decryption_keys.pop(0)
                i = 0
                for b in chunk:
                    b_xor = chr(ord(b) ^ ord(dec_key[i]))
                    ret += b_xor
                    i += 1
            else:
                ret += chunk
        return ret
