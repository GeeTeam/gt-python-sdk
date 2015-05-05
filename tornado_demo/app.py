# coding:utf-8
import tornado.ioloop
import tornado.web
import tornado.gen
import sdk.geetest as geetest


BASE_URL = "api.geetest.com/get.php?gt="

captcha_id = "a40fd3b0d712165c5d13e6f747e948d4"
private_key = "0f1a37e33c9ed10dd2e133fe2ae9c459"
product = "embed"

# 弹出式
# product = "popup&popupbtnid=submit-button"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        gt = geetest.geetest(captcha_id, private_key)
        url = ""
        httpsurl = ""
        try:
            challenge = gt.geetest_register()
        except:
            challenge = ""
        if len(challenge) == 32:
            url = "http://%s%s&challenge=%s&product=%s" % (BASE_URL, captcha_id, challenge, product)
            httpsurl = "https://%s%s&challenge=%s&product=%s" % (BASE_URL, captcha_id, challenge, product)
        self.render("static/login.html", url=url)

    def post(self):
        username = self.get_argument("email")
        password = self.get_argument("password")
        challenge = self.get_argument("geetest_challenge")
        validate = self.get_argument("geetest_validate")
        seccode = self.get_argument("geetest_seccode")
        # print challenge
        # print seccode
        # print validate
        gt = geetest.geetest(captcha_id, private_key)
        result = gt.geetest_validate(challenge, validate, seccode)
        if result:
            self.write("success")
        else:
            self.write("fail")

if __name__ == "__main__":
    app = tornado.web.Application([
                                      (r"/", MainHandler),
                                  ], debug=True)

    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
