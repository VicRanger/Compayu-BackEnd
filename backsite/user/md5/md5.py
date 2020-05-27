import hashlib


# 返回md5加密后的字符串
def md5(pw):
    ret = hashlib.md5(pw.encode(encoding='UTF-8')).hexdigest()
    return ret
