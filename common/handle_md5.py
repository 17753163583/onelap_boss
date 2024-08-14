import hashlib


def md5_encrypt(origin_passwd):
    md5 = hashlib.md5()
    md5.update(str(origin_passwd).encode('utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    print(md5_encrypt('zhang107'))
