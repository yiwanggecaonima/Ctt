import time
import requests
import urllib.request
from urllib.error import URLError
import re

def get_proxy():
    headers = {'User_Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    try:
        request = urllib.request.Request("...", headers=headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode()
        response.close()
        ip_port = data.strip("\r\n").split(':')
        print(ip_port)
        if '设置为白名单' in data:
            ret = re.compile(r'请将(.*)设置为白名单')
            ip = re.findall(ret, data)[0]
            print(ip, type(ip))
            white_ip = '...' + ip
            result = requests.get(white_ip, headers=headers)
            if '保存成功' in result.text:
                print('白名单保存成功')
                return get_proxy()
        elif '您的套餐pack传参有误' in data:
            ret = re.compile(r'请检测您现在的(.*)是否在套餐')
            ip = re.findall(ret, data)[0]
            print(ip, type(ip))
            white_ip = '...' + ip
            result = requests.get(white_ip, headers=headers)
            if '保存成功' in result.text:
                print('白名单保存成功')
                return get_proxy()
        elif '秒后再次请求' in data:
            time.sleep(3)
            return get_proxy()
        return ip_port
    except urllib.error.URLError as e:
        print("wait ......",e)
        time.sleep(5)
        return get_proxy()
