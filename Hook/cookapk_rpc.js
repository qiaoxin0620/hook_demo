rpc.exports = {
    getToken : function (str) {
        send("getToken rpc")
        Java.perform(function () {
                //拿到context上下文
                var currentApplication = Java.use("android.app.ActivityThread").currentApplication();
                var context = currentApplication.getApplicationContext();

                var AuthUtils = Java.use("com.coolapk.market.util.AuthUtils");
                var token = AuthUtils.getAS(context,str);
                send(token);
            }
        )
    }
}