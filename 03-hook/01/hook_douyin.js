rpc.exports = {
    getsign: function (timestamp, url, device_info, device_id) {
        var sign = "";
        Java.perform(
            function () {
                var UserInfo = Java.use("com.ss.android.common.applog.UserInfo");
                var GlobalContext = Java.use("com.ss.android.common.applog.GlobalContext");
                var AwemeApplication = Java.use("com.ss.android.ugc.aweme.app.AwemeApplication");
                var StcSDKFactory = Java.use("com.ss.sys.ces.out.StcSDKFactory");
                var EagleEye = Java.use("com.ss.android.common.applog.EagleEye");

                var sdk = StcSDKFactory.getSDK(GlobalContext.getContext(), AwemeApplication.p().m());

                var usrInfo = UserInfo.getUserInfo(timestamp, url, device_info, device_id);

                var ac = str.substr(0,22);
                var cp = str.substr(22,usrInfo.length);
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
    var bytes = []
    for (var i = 0; i < s; i++) {
        bytes.push(s.charCodeAt(i));
    }
    return bytes;
}


Java.perform(
    function () {
        var userinfo = Java.use("com.ss.android.common.applog.UserInfo");
        userinfo.getUserInfo.implementation = function (v1, v2, v3, v4) {
            send(v1);
            send(v2);
            send(v3);
            send(v4);
            this.getUserInfo(v1, v2, v3, v4);
        };
    }
)