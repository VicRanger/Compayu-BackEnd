import json
import requests

from backsite.settings import APIKEY


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【蒲赠霖】欢迎注册，您的手机验证码是{code}。验证码5分钟内有效。".format(code=code)
        }
        response = requests.post(self.single_send_url, data=parmas)  # 返回response.text的实际上是字符串
        re_dict = json.loads(response.text)  # 所以需要解析response.text
        return re_dict


'''
if __name__ == "__main__":  # 用来测试发送功能，当DRF提供了相应的接口后，可以注释掉
    yun_pian = YunPian(APIKEY)
    yun_pian.send_sms("111111", "18144223419")  # 因为是测试用，所以静态数据即可
'''
