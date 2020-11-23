import frida,sys

def on_message(message,data):
    if message["type"] == 'send':
        print("[*]{0}".format(message["payload"]))
    else:
        print(message)


# jscode = """
# Java.perform(
#  function () {
#     var v = Java.androidVersion;
#     send('version:'+v);
#
#     var classnames = Java.enumerateLoadedClassesSync();
#
#     for(var i=0; i< classnames.length;i++){
#         send('class name:'+classnames[i]);
#     };
# }
# );
# """

jscode = """
Java.perform(
 function () {
    var classname = Java.use('com.yaotong.crackme.MainActivity');
    classname.securityCheck.implementation = function() {
      send("function hook");
      return true;
    }
}
);
"""

process = frida.get_usb_device().attach("com.yaotong.crackme")
script = process.create_script(jscode)
script.on("message",on_message)
print("[*] Runing CTF")
script.load()
sys.stdin.read()