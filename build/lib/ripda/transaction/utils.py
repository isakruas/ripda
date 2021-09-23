import hashlib


class Utils:

    @staticmethod
    def sha256(string):
        _sha256 = hashlib.sha256(string.encode('utf-8'))
        return _sha256.hexdigest()

    @staticmethod
    def ripemd160(string):
        _ripemd160 = hashlib.new('ripemd160')
        _ripemd160.update(string.encode('utf-8'))
        return _ripemd160.hexdigest()
