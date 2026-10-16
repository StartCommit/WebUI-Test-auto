import base64
import hashlib
import hmac
import time
import urllib.parse
import requests

from util_tools.handle_data.configParse import ConfigParse

conf = ConfigParse()


def generate_sign():
    """
    生成加密标签
    :return:
    """
    # 获取当前时间的时间戳
    timestamp = str(int(time.time() * 1000))
    # 获取钉钉机器人里面的加密秘钥
    secret = conf.get_section_ding('secret')
    # 转码成utf-8
    secret_enc = secret.encode('utf-8')
    # 组合当前时间戳和密钥
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    # 转成byte类型
    string_to_sign_enc = string_to_sign.encode('utf-8')
    # 通过加密方式加密当前时间戳和密钥
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_dd_msg(content_strm, at_all=True):
    """
    发送钉钉消息
    :param content_strm:
    :param at_all:
    :return:
    """
    timestamp, sign = generate_sign()
    # 组合一个完整的url地址
    url = f"{conf.get_section_ding('webhook')}&timestamp={timestamp}&sign={sign}"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {
        "msgtype": "text",
        "text": {
            "content": content_strm
        },
        "at": {
            "isAtAll": at_all
        }
    }
    res = requests.post(url, json=data, headers=headers)
    return res.text
