import frida
import sys

def on_message(message,data):
    if message['type'] == "send":
        print("[*]{0}".format(message["payload"]))
    else:
        print(message)


hook_coolapk = '''
    // so文件的基地址 程序运行起来会变化
    // 函数的绝对地址 = so文件的基地址 + 函数偏移量  ===>  静态分析的时候知道函数的偏移量，然后就可以hook出运行时的某个函数的地址，来算出so文件的基地址
    var getAuthString_absulate_add = Module.findExportByName("libnative-lib.so","getAuthString");  //获取getAuthString函数的绝对地址
    var native_lib_base_add = parseInt(getAuthString_absulate_add) - parseInt("0x66500");
    send("native_lib_base_add:" + ptr(native_lib_base_add));
    
    // 用libnative-lib.so基地址加上MD5：MD5的偏移量就是MD5：MD5在内存中的地址
    var md5_init_address = ptr(native_lib_base_add + parseInt("0x32168"));
    send("md5_init_address:" + md5_init_address);
    
    // hook MD5:MD5()
    //hook bs64_encode
    var bs64_init_address = ptr(native_lib_base_add + parseInt("0x31DB8"));
    send("bs64_init_address:" + bs64_init_address);
    
    Interceptor.attach(bs64_init_address, 
    {
        onEnter: function(args) {
             send("b64_encode ori:" + Memory.readUtf8String(args[0]));
        },
        onLeave:function(retval){
            send("retval:"+retval);
        }
    });
'''

process = frida.get_usb_device(-1).attach('com.coolapk.market')
script = process.create_script(hook_coolapk)
script.on('message', on_message)
print('[*] Running CTF')
script.load()
sys.stdin.read()