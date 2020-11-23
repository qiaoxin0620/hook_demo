import frida
import sys
import os
def adbForward():
    os.system("adb forward tcp:27042 tcp:27042")
    os.system("adb forward tcp:27043 tcp:27043")


def message_on(message,data):
    if message['type'] == "send":
        print("[*]{}".format(message["payload"]))
        return message["payload"]
    else:
        pass

hook_coolapk_rpc = '''
rpc.exports = {
    gettoken : function (str) {
        var token = "";
        send("getToken rpc")
        Java.perform(function () {
                //拿到context上下文
                var currentApplication = Java.use("android.app.ActivityThread").currentApplication();
                var context = currentApplication.getApplicationContext();
                
                var AuthUtils = Java.use("com.coolapk.market.util.AuthUtils");
                token = AuthUtils.getAS(context,str);
                send(token);
                
            }
        )
        return token;
    }
};
'''


adbForward()
process = frida.get_usb_device(-1).attach("com.coolapk.market")
script = process.create_script(hook_coolapk_rpc)
script.on("message",message_on)
print('[*] Running CTF')
script.load()
device_id = "28402afe-17ed-3c1e-8367-d1298a53005f"
token = script.exports.gettoken(device_id)
print("main:",token)