import hashlib
import time
import uuid

import requests
import json
from base64 import b64encode

def get_token(device_id):
    timestamp = int(time.time())
    v62 = f"token://com.coolapk.market/c67ef5943784d09750dcfbb31020f0ab?{hashlib.md5(str(timestamp).encode()).hexdigest()}${device_id}&com.coolapk.market"
    token = f"{hashlib.md5(b64encode(v62.encode())).hexdigest()}{device_id}{hex(timestamp)}"
    return token

def get_app_token(device_id,timestamp):
    DEVICE_ID = uuid.uuid4()
    t = int(time.time())
    hex_t = hex(t)
    # 时间戳加密
    md5_t = hashlib.md5(str(t).encode('utf-8')).hexdigest()
    # 不知道什么鬼字符串拼接
    a = 'token://com.coolapk.market/c67ef5943784d09750dcfbb31020f0ab?{}${}&com.coolapk.market'.format(md5_t, DEVICE_ID)

    md5_a = hashlib.md5(b64encode(a.encode('utf-8'))).hexdigest()
    token = '{}{}{}'.format(md5_a, DEVICE_ID, hex_t)
    # print(token)
    return token

def get_x_app_token(device_id,timestamp):
    md_time = hashlib.md5(str(timestamp).encode("utf-8")).hexdigest()
    base_pre = f"token://com.coolapk.market/c67ef5943784d09750dcfbb31020f0ab?{md_time}${device_id}&com.coolapk.market".encode("utf-8")
    token = f"{hashlib.md5(b64encode(base_pre)).hexdigest()}{device_id}{hex(timestamp)}"
    print(token)
    return token

if __name__ == '__main__':

    # m = hashlib.md5()
    # timestamp = int(time.time())
    # m.update(str(timestamp).encode("utf-8"))
    # md_time = m.hexdigest()
    # base_pre = f"token://com.coolapk.market/c67ef5943784d09750dcfbb31020f0ab?{md_time}$28402afe-17ed-3c1e-8367-d1298a53005f&com.coolapk.market".encode("utf-8")
    # base_str = b64encode(base_pre)
    # m = hashlib.md5()
    # m.update(base_str)
    # md5_base_str = m.hexdigest()
    # x_token = md5_base_str + "28402afe-17ed-3c1e-8367-d1298a53005f" + hex(timestamp)
    # print("mine:",x_token)
    # device_id = "28402afe-17ed-3c1e-8367-d1298a53005f"
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 6P Build/MTC20L) (#Build; google; Nexus 6P; MTC20L; 6.0.1) +CoolMarket/9.2.2-1905301",
        "X-Requested-With": "XMLHttpRequest",
        "X-Sdk-Int": "23",
        "X-Sdk-Locale": "zh-CN",
        "X-App-Id": "com.coolapk.market",
        "X-App-Token": "d6732c5ba2a038d3d2cc6ab65d034f5d28402afe-17ed-3c1e-8367-d1298a53005f0x5f93aedf",
        "X-App-Version": "9.2.2",
        "X-App-Code": "1905301",
        "X-Api-Version": "9",
        "X-App-Device": "AU2Ayc1hXZOByOlx2Zv92ZgsTaldXY1hEI7gTO6gTO6MUR6EEM6gjN6ATNgsDbsVnbgsDbsVnbgsDN2ImM5EWY0YTNlNzYiBTZ",
        "X-Dark-Mode": "0", }
    # for i in range(100):
    #     timestamp = int(time.time())
    #     device_id = uuid.uuid4()
    #     x_token = get_x_app_token(device_id, timestamp)
    #     url = f"https://api.coolapk.com/v6/page/dataList?url=V9_HOME_TAB_FOLLOW&title=%E5%85%B3%E6%B3%A8&page={i}&lastItem=22392890"
    #     res = requests.get(url, headers=headers)
    #     # "https://api.coolapk.com/v6/page/dataList?url=V9_HOME_TAB_FOLLOW&title=%E5%85%B3%E6%B3%A8&page=9&lastItem=22392408"
    #     if res.status_code == 200:
    #         print(res.text)
    #         print(json.loads(res.text))

    # headers.update({"X-App-Token":x_token})
    url = "https://api.coolapk.com/v6/page/dataList?url=V9_HOME_TAB_FOLLOW&title=%E5%85%B3%E6%B3%A8&page=8&lastItem=22392890"
    res = requests.get(url,headers=headers)
    # "https://api.coolapk.com/v6/page/dataList?url=V9_HOME_TAB_FOLLOW&title=%E5%85%B3%E6%B3%A8&page=9&lastItem=22392408"
    if res.status_code == 200:
        print(res.text)
        print(json.loads(res.text))

