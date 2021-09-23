import hashlib


def sha256(data, is_bytes: bool = False):
    if is_bytes:
        return hashlib.sha256(data).digest()
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
