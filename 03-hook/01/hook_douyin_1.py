import frida, sys
import time

hook_code = """
rpc.exports = {
    getsig:function(timstamp ,url, userinfo_array, device_id){
        var sig = "";

        Java.perform(
            function(){
                var UserInfo = Java.use('com.ss.android.common.applog.UserInfo');
                var EagleEye = Java.use('com.ss.android.common.applog.EagleEye');
                var StcSDKFactory = Java.use('com.ss.sys.ces.out.StcSDKFactory');
                var GlobalContext = Java.use('com.ss.android.common.applog.GlobalContext');
                var AwemeApplication = Java.use('com.ss.android.ugc.aweme.app.AwemeApplication');

                var sdk = StcSDKFactory.getSDK(GlobalContext.getContext(), AwemeApplication.p().m())

                var usrInfo = UserInfo.getUserInfo(timstamp, url, userinfo_array, device_id);

                var as = usrInfo.substring(0, 22);
                var cp = usrInfo.substring(22, usrInfo.length);
                var mas = EagleEye.byteArrayToHexStr(sdk.encode(getBytes(as)));

                //send('as:'+as);
                //send('cp:'+cp);
                //send('mas:'+mas);
                sig = '&as='+as+'&cp='+cp+'&mas='+mas;
            }
        )
        return sig;
    }
}

function getBytes(s) {
        var bytes = [];
            for (var i = 0; i < s.length; i++) {
                bytes.push(s.charCodeAt(i));
            }
        return bytes;
}


"""


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


def get_sig_hook(script):
    print('repose')
    timestamp_w = time.time()
    timestamp = int(timestamp_w)
    device_id = 69852570923
    infos = ['sdk_version', '1.3.0', 'ts', str(timestamp), 'app_type', 'lite', 'os_api', '23', 'device_type',
             'Nexus 6P',
             'device_platform', 'android', 'ssmix', 'a', 'iid', '91658564592', 'manifest_version_code', '203', 'dpi',
             '560',
             'version_code', '203', 'app_name', 'douyin_lite', 'version_name', '2.0.3', 'openudid', 'dd08f504420bcde0',
             'device_id', str(device_id), 'resolution', '1440*2392', 'os_version', '6.0', 'language', 'zh',
             'device_brand', 'google',
             'ac', 'wifi', 'update_version_code', '2030', 'aid', '2329', 'channel', 'xiaomi', '_rticket',
             str(timestamp_w)]
    # infos1 = "sdk_version,1.3.0"
    url = 'https://iu.snssdk.com/location/locate/?sdk_version=1.3.0&ts={}&app_type=lite&os_api=23&device_type=Nexus 6P&device_platform=android&ssmix=a&iid=91658564592&manifest_version_code=203&dpi=560&version_code=203&app_name=douyin_lite&version_name=2.0.3&openudid=dd08f504420bcde0&device_id=69852570923&resolution=1440*2392&os_version=6.0&language=zh&device_brand=google&ac=wifi&update_version_code=2030&aid=2329&channel=xiaomi&_rticket={}'.format(
        timestamp, timestamp_w)


    # print(','.join(infos))
    sig = script.exports.getsig(timestamp, url, infos, str(device_id))
    print('sig:', sig)
    return sig


def get_sig(script, timestamp, url, infos, device_id):
    return script.exports.getsig(timestamp, url, infos, str(device_id))


# def prepare_hook():
process = frida.get_usb_device().attach('com.ss.android.ugc.aweme.lite')
script = process.create_script(hook_code)
script.on('message', on_message)
script.load()
get_sig_hook(script)

# get_sig_hook(script)

# return script
