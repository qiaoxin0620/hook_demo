import os

import frida
import sys
import requests
import time

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

def adbForward():
    os.system("adb forward tcp:27042 tcp:27042")
    os.system("adb forward tcp:27043 tcp:27043")

'''
1.抓包分析。如果抓取不到包。可能app有ssl证书校验。安装justTrustMe来抓包，如果不行安装justmeplus抓包，还不行就用ssl_logger.py来抓取ssl层的包，然后用wireshark打开。
2.抓包完成后分析请求参数。哪些变化，哪些不变化。然后提取出变化的参数。
3.用jadx反编译apk文件，看是否有加固。如果加固就用Fdex2脱壳。可能要重启多次重启机器。多次安装apk
4.将反编译好的dex文件搞到本地。/data/user/0/packge/*.dex  注意：需要chmod 777 权限
5.用jadx打开.dex文件，查找加密参数的关键字。 记得用 "key  "&key= ”key =  XX.key,  “.key,
6.找到函数。hook函数，看函数传入的参数。可以先dp.fun.implementation = function(param...){}  打印参数。根据提示加上overload参数重载函数
7.编写rpc函数。

'''
hook_tianyancha = '''
    Java.perform(
    function () {
        var dp = Java.use("com.tianyancha.skyeye.utils.dp");
        dp.a.overload('java.lang.String', 'java.lang.String', 'java.lang.String', 'java.lang.String', 'java.lang.String', 'java.lang.String').implementation = function (v1,v2,v3,v4,v5,v6) {
            send(v1);
            send(v2);
            send(v3);
            send(v4);
            send(v5);
            send(v6);
            this.a(v1,v2,v3,v4,v5,v6);
        }
    }
);
'''

hook_tianyancha_rpc = '''
rpc.exports = {
    getparam:function (url,version) {
        var param = {"duid":"","authorization":"","tyc-hi":"","device_id":""};
        Java.perform(function () {
            var dp = Java.use("com.tianyancha.skyeye.utils.dp");
            var authorization = dp.I();
            var duid = dp.g();
            var device_id = dp.i();
            var tyc = dp.a(url, authorization, version, "", device_id, "slat");
            param["duid"] = duid
            param["authorization"] = authorization;
            param["tyc-hi"] = tyc;
            param["device_id"] = device_id;
            }
        );
        return param;
    }
}
'''

process = frida.get_usb_device().attach('com.tianyancha.skyeye')
script = process.create_script(hook_tianyancha_rpc)
script.on('message', on_message)
script.load()
# sys.stdin.read()
url = "https://api4.tianyancha.com/services/v3/t/details/appComIcV4/9519792?pageSize=1000"
version = "Android 11.4.0"
param = script.exports.getparam(url,version)
print(param)
# request_page(script)