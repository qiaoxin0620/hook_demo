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


hook_douyin = '''
Java.perform(
    function(){
        var userinfo = Java.use("com.ss.android.common.applog.UserInfo");
        userinfo.getUserInfo.overload('int', 'java.lang.String', '[Ljava.lang.String;', 'java.lang.String').implementation = function(v1,v2,v3,v4){
            send(v1);
            send(v2);
            send(v3);
            send(v4);
            var str = this.getUserInfo(v1,v2,v3,v4);
            send(str);
            return str;
            
         };
    }
)
'''

hook_douyin_rpc = '''
rpc.exports = {
    getsign : function (ts,url,device_info,device_id) {
        var sign = "";
        send("getsign rpc")
        Java.perform(function () {
                var UserInfo = Java.use("com.ss.android.common.applog.UserInfo");
                var GlobalContext = Java.use("com.ss.android.common.applog.GlobalContext");
                var AwemeApplication = Java.use("com.ss.android.ugc.aweme.app.AwemeApplication");
                var StcSDKFactory = Java.use("com.ss.sys.ces.out.StcSDKFactory");
                var EagleEye = Java.use("com.ss.android.common.applog.EagleEye");

                var sdk = StcSDKFactory.getSDK(GlobalContext.getContext(), AwemeApplication.p().m());

                var usrInfo = UserInfo.getUserInfo(ts,url,device_info,device_id);

                var ac = usrInfo.substr(0,22);
                var cp = usrInfo.substr(22,usrInfo.length);
                var mas = EagleEye.byteArrayToHexStr(sdk.encode(getBytes(usrInfo)));
                send("ac="+ac);
                send("cp="+cp);
                send("mas="+cp);
                sign = "&ac="+ac + "&cp="+cp + "&mas="+mas
            }
        )
        return sign;
    }
}

function getBytes(s){
    var bytes = [];
    for (var i = 0; i < s.length; i++) {
        bytes.push(s.charCodeAt(i));
    }
    return bytes;
}
'''




def request_page(rpc):
    ts = int(time.time())
    _rticket = str(int(time.time() * 1000))
    url = f"https://api.amemv.com/aweme/v1/challenge/aweme/?ch_id=1623977388448775&query_type=0&cursor=0&count=20&type=5&retry_type=no_retry&iid=3377327402659437&device_id=3359718008690942&ac=wifi&channel=xiaomi&aid=2329&app_name=douyin_lite&version_code=203&version_name=2.0.3&device_platform=android&ssmix=a&device_type=Nexus+6P&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=e0bc3e564aa92b64&manifest_version_code=203&resolution=1440*2392&dpi=560&update_version_code=2030&_rticket={_rticket}&ts={str(ts)}"
    device_id = "3359718008690942"
    device_info = ['sdk_version', '1.3.0', 'ts', str(ts), 'app_type', 'lite', 'os_api', '23', 'device_type',
                   'Nexus 6P', 'device_platform', 'android', 'ssmix', 'a', 'iid', '3377327402659437',
                   'manifest_version_code', '203', 'dpi', '560', 'version_code', '203', 'app_name', 'douyin_lite',
                   'version_name', '2.0.3', 'openudid', 'e0bc3e564aa92b64', 'device_id', device_id,
                   'resolution', '1440*2392', 'os_version', '6.0.1', 'language', 'zh', 'device_brand', 'google', 'ac',
                   'wifi', 'update_version_code', '2030', 'aid', '2329', 'channel', 'xiaomi', '_rticket',
                   _rticket]
    ac_cp_mas = rpc.exports.getsign(ts,url,device_info,device_id)
    headers = {
        'Host': 'api.amemv.com',
        'User-Agent': 'com.ss.android.ugc.aweme.lite/203 (Linux; U; Android 6.0.1; zh_CN; Nexus 6P; Build/MTC20L; Cronet/58.0.2991.0)',
    }
    url = url + ac_cp_mas
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.text)


# process = frida.get_usb_device(-1).attach('com.ss.android.ugc.aweme.lite');
# script = process.create_script(hook_douyin)
# script.on('message', on_message)
# print('[*] Running CTF')
# script.load()
# sys.stdin.read()

process = frida.get_usb_device(-1).attach("com.ss.android.ugc.aweme.lite")
script = process.create_script(hook_douyin_rpc)
script.on("message",on_message)
print('[*] Running CTF')
script.load()
request_page(script)

# timestamp_w = time.time()
# timestamp = int(timestamp_w)
# url = f"https://api.amemv.com/aweme/v1/challenge/aweme/?ch_id=1623977388448775&query_type=0&cursor=0&count=20&type=5&retry_type=no_retry&iid=3377327402659437&device_id=3359718008690942&ac=wifi&channel=xiaomi&aid=2329&app_name=douyin_lite&version_code=203&version_name=2.0.3&device_platform=android&ssmix=a&device_type=Nexus+6P&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=e0bc3e564aa92b64&manifest_version_code=203&resolution=1440*2392&dpi=560&update_version_code=2030&_rticket={timestamp}&ts={timestamp}"
# print()
# device_id = "3359718008690942"
# device_info = ['sdk_version', '1.3.0', 'ts', str(timestamp), 'app_type', 'lite', 'os_api', '23', 'device_type',
#                'Nexus 6P', 'device_platform', 'android', 'ssmix', 'a', 'iid', '3377327402659437',
#                'manifest_version_code', '203', 'dpi', '560', 'version_code', '203', 'app_name', 'douyin_lite',
#                'version_name', '2.0.3', 'openudid', 'e0bc3e564aa92b64', 'device_id', device_id,
#                'resolution', '1440*2392', 'os_version', '6.0.1', 'language', 'zh', 'device_brand', 'google', 'ac',
#                'wifi', 'update_version_code', '2030', 'aid', '2329', 'channel', 'xiaomi', '_rticket',str(timestamp)]
# ac_cp_mas = script.exports.getsign(timestamp,url,device_info,device_id)
# print("hahahah")
# print(ac_cp_mas)
# print("kong")

