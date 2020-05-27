import time
import base64
import hmac
from datetime import datetime, timedelta

# 加密获得token的方法
# 过期时间设置为半个小时
from user import models


def get_token(key, expire=1800):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


# 解密token的方法
# 返回布尔值判断是否匹配
def out_token(key, token):
    # token是前端传过来的token字符串
    try:
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if float(ts_str) < time.time():
            # token expired
            return False
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            # token certification failed
            return False
        # token certification success
        return True
    except Exception as e:
        print(e)


# 根据token值返回用户id
# 0 - 没找到 ； -1 - 过期了
def getUserByToken(token):
    token = models.UserToken.objects.filter(token=token)
    if token.count() == 0:
        return 0
    else:
        token = token.first()
        if datetime.now() > token.expiration_time:
            return -1
        else:
            # 返回用户
            return token.user_id
