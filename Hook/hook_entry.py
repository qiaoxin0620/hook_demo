import frida
import sys

oncreate_script = """
//打印调用堆栈
function printStack(){
    send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
}

//array转换成string
function array2string(array){
    var buffer = Java.array('byte',array);
    var result = ""
    for(var i=0;i<buffer.length;i++){
        result += (String.fromCharCode(buffer[i]));
    }
    return result;
}

Java.perform(
    function(){
        var MessageDigest = Java.use("java.security.MessageDigest");
        
        MessageDigest.update.overload('[B').implementation = function(bytesarray){
            send('I am hera 0:');
            send("ori:"+array2string(bytesarray));
            printStack();
            this.update(bytesarray);
        },
        MessageDigest.update.overload('byte').implementation = function(bytesarray){
            send('I am hera 1:');
            //send("ori:"+array2string(bytesarray));
            //printStack();
            this.update(bytesarray);
        },
        MessageDigest.update.overload('java.nio.ByteBuffer').implementation = function (bytesarray) {
            send('I am here 2:');
            //var String = Java.use('java.lang.String').$new(bytesarray);
            //send("ori:"+array2string(bytesarray));
            //printstack();
            this.update(bytesarray);
        },
        MessageDigest.update.overload('[B', 'int', 'int').implementation = function (bytesarray) {
            send('I am here 3:');
            //var String = Java.use('java.lang.String').$new(bytesarray);
            //send("ori:"+array2string(bytesarray));
            //printstack();
            this.update(bytesarray);
        },
        MessageDigest.getInstance.overloads[0].implementation = function(algorithm) {
            send("call ->getInstance for " + algorithm);
            return this.getInstance.overloads[0].apply(this, arguments);
        };
        
    }
);
"""


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

device = frida.get_usb_device()
pid = device.spawn(['com.iCitySuzhou.suzhou001'])
process = device.attach(pid)

script = process.create_script(oncreate_script)
script.on('message', on_message)
print('[*] Running CTF')
script.load()
device.resume(pid)
sys.stdin.read()
