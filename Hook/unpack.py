import frida
import sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

open_memory_6 = "_ZN3art7DexFile10OpenMemoryEPKhjRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPNS_6MemMapEPKNS_10OatDexFileEPS9_"

# OpenMemory 在安卓/system/lib/libart.so文件中，用IDA 32打开，然后Ctrl + F 查找方法名OpenMemory，然后按F5查看源码，在OpenMemory右键edit func 查看函数名
# Hook OpenMemory的导出方法名
# 用IDA 打开libart.so 查看OpenMemory的导出方法名 【查找方法名，并在代码编辑框按F5，右键方法名查看导出方法名】
# OpenMemory的第一个参数是dex文件在内存中的起始位置
# 根据dex文件格式 从起始位置开始 第32个字节 是该dex文件的大小
# 知道dex起始位置和整个文件大小，只需要把这段内存dum出来即可
# 适用于 安卓 6 7 8 9

#文件的起始位置 文件的大小 知道了文件的结束位置
oncreate_script = """
Java.perform(
    function () {
        var TestSig = Java.use('com.yaotong.crackme.MainActivity');

        TestSig.onCreate.overload('android.os.Bundle').implementation = function (v) {
            send('I am here');
            this.onCreate();
        };
    }
);
"""

package = "com.iCitySuzhou.suzhou001"

src = """
var openMemory_address = Module.findExportByName("libart.so","_ZN3art7DexFile10OpenMemoryEPKhjRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPNS_6MemMapEPKNS_10OatDexFileEPS9_");
send("openMemory address:" + openMemory_address);
Interceptor.attach(openMemory_address,{
    onEnter:function(args){
        //dex文件的起始位置
        var dex_begin_address = args[1]
        
        //dex文件的前8个字节是magic字段，看dex的文件格式说明
        //打印magic（会显示“dex 035”）三个字符 可以验证是否为dex文件
        console.log("magic:" + Memory.readUtf8String(dex_begin_address));
        
        //把地址转换成整数 在加上32
        //因为dex文件的第32个字节处存放的是dex文件大小
        var address = parseInt(dex_begin_address,16) + 0x20;
        
        //把address地址指向的内存值读出来，改值就是dex文件的大小
        //ptr(address)转换的原因是 frida只接受 NativePointer类型指针
        var dex_size = Memory.readInt(ptr(address));
        console.log("dex size:"+ dex_size);
        
        //frida 写文件 把内存中的数据写到本地
        var timestamp = new Date().getTime();
        var file = new File("/data/data/%s/" + timestamp + ".dex","wb")
        //把内存里的数据读出来，从begin开始读取，读取length长度
        file.write(Memory.readByteArray(dex_begin_address,dex_size))
        file.flush()
        file.close()
        
        send("dex begin address:" + parseInt(dex_begin_address,16))
        send("dex file size:" + dex_size)
    },
    onLeave:function(retval){
        if(retval.toInt32()>0){
        }
    }
});
"""%package


print("dex 导出目录为: /data/data/%s"%(package))
device = frida.get_usb_device()
pid = device.spawn(package)
session = device.attach(pid)
script = session.create_script(src)
script.on("message" , on_message)
script.load()
device.resume(pid)
sys.stdin.read()