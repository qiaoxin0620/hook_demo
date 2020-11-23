Java.perform(
    function () {
        var dp = Java.use("com.tianyancha.skyeye.utils.dp");
        dp.a.implementation = function (v1,v2,v3,v4,v5,v6) {
            send(v1);
            send(v2);
            send(v3);
            send(v4);
            send(v5);
            send(v6);
        }
    }
)

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

rpc.exports = {
    xx : function (xx,xx) {
        Java.perform(function () {
            // do something
        })
    }
}