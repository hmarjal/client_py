import secrets


def generate_keys() -> list:
    encrpytion_keys = []
    for n in range(20):
        encryption_word = secrets.token_bytes(64)
        encrpytion_keys.append(encryption_word)
    return encrpytion_keys
